from collections import Counter
from functools import reduce
import operator

BILABIAL = (0, {'positive': ['labial'], 'negative': ['syllabic']})
APICAL = (1, {'positive': ['coronal', 'anterior'], 'negative': ['syllabic']})
PALATAL = (2, {'positive': ['distributed'], 'negative': ['anterior', 'syllabic']})
VELAR = (3, {'positive': ['dorsal'], 'negative': ['syllabic']})
GLOTTAL = (4, {'negative': ['labial', 'syllabic', 'coronal', 'dorsal']})

FRONT = (5, {'positive': ['front'], 'negative': ['back']})
CENTRAL = (6, {'negative': ['front', 'back']})
BACK = (7, {'positive': ['back'], 'negative': ['front']})

PHONETIC_CONSTANTS = [BILABIAL, APICAL, PALATAL, VELAR, GLOTTAL, FRONT,
                      CENTRAL, BACK]


def classify_segment(segment):
    '''Given a segment, return all phonetic constants which apply to it, in a
    list.'''
    return [constant[0] for constant in PHONETIC_CONSTANTS if
            segment.meets_conditions(constant[1])]


def phonetic_product(word):
    '''Given a word, compute the Phonetic Product outlined by Harold Bauer &
    Michael P. Robb in "The ethologic model of phonetic development" (1992).

    '''
    phonetic_count = Counter()

    for segment in word.segments:
        phonetic_count.update(classify_segment(segment))

    return reduce(operator.mul, map(lambda x: x + 1, phonetic_count.values()))
