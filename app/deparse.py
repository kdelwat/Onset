from Levenshtein import distance

import csv

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


def best_segment_match(target_feature_string, all_feature_strings):
    '''Returns the best match for the segment denoted by the target feature string,
    from the given list of tuples containing feature strings. The first item in
    each tuple is the phoneme and the second is the feature string.

    '''

    # Record the Levenshtein distance between each feature string and the
    # target.
    ranked_options = [(distance(target_feature_string, string[1]), string) for
                      string in all_feature_strings]

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


def deparse_words(words, segments, diacritics):
    '''Given a list of Words, return a list of IPA strings, one for each
    word.'''

    # Load feature strings
    with open('data/hayes-feature-strings.csv', 'r') as f:
        feature_strings = list(csv.reader(f))

    # Load diacritic data into a dictionary. The keys are the features while
    # the values are the corresponding IPA.
    with open('data/simple_diacritics.csv', 'r') as f:
        diacritics = {line[1]: line[0] for line in csv.reader(f)}

    word_strings = []

    for word in words:
        word_string = ''

        for segment in word.segments:
            segment_string = best_segment_match(feature_string(segment),
                                                feature_strings)

            for diacritic_feature in segment.diacritics:
                segment_string += diacritics[diacritic_feature]

            word_string += segment_string

        word_strings.append(word_string)

    return word_strings
