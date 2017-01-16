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


def deparse_words(words, segments, diacritics):
    pass
