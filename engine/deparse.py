from functools import partial
from collections import defaultdict
from Levenshtein import distance

feature_order = ['syllabic',
                 'stress',
                 'long',
                 'consonantal',
                 'sonorant',
                 'continuant',
                 'delayedrelease',
                 'approximant',
                 'tap',
                 'trill',
                 'nasal',
                 'voice',
                 'spreadglottis',
                 'constrictedglottis',
                 'labial',
                 'round',
                 'labiodental',
                 'coronal',
                 'anterior',
                 'distributed',
                 'strident',
                 'lateral',
                 'dorsal',
                 'high',
                 'low',
                 'front',
                 'back',
                 'tense']


def feature_string(segment):
    '''Convert a Segment object into a feature string.'''
    features = []

    for feature in feature_order:
        if feature in segment.positive:
            features.append('+')
        elif feature in segment.negative:
            features.append('-')
        else:
            features.append('0')

    return ''.join(features)


def segment_match(feature_strings, target_segment):
    '''Returns the best match for the IPA string of the given Segment, from the
    given list of tuples containing feature strings. The first item in each
    tuple is the phoneme and the second is the feature string.

    '''
    target_feature_string = feature_string(target_segment)

    # Build a dictionary, where each key is the Levenshtein distance between
    # all strings in its list and the target feature string.
    distances = defaultdict(list)

    for string in feature_strings:
        distances[distance(target_feature_string, string[1])].append(string[0])

    # Get all feature strings with the lowest distance
    lowest_feature_strings = distances[min(distances.keys())]

    # Return the shortest of these strings, because we want to deparse
    # into the simplest segments possible.
    return min(lowest_feature_strings, key=len)


def deparse_words(words, segments, feature_strings):
    '''Given a list of Words, return a list of IPA strings, one for each
    word.'''

    # Partially apply the segment_match function to avoid repeated calls with
    # the feature_strings object.
    deparse = partial(segment_match, feature_strings)

    # Deparse each segment in each word
    word_strings = [''.join(deparse(segment) for segment in word.segments)
                    for word in words]

    return word_strings
