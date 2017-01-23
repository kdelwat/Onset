from functools import partial
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

    # Record the Levenshtein distance between each feature string and the
    # target.
    ranked_options = [(distance(target_feature_string, string[1]), string) for
                      string in feature_strings]

    # Sort based on distance between the strings.
    ranked_options.sort(key=lambda x: x[0])

    # Remove all options that don't have the current lowest distance
    lowest = ranked_options[0][0]
    lowest_options = [option for option in ranked_options if option[0] ==
                      lowest]

    # Sort by length of the segment, as we want the simplest possible segment.
    lowest_options.sort(key=lambda x: len(x[1][0]))

    # Return the first remaining segment
    return lowest_options[0][1][0]


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
