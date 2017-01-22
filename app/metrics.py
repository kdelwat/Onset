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
    '''Given a word, compute the Phonetic Product outlined by Harold R. Bauer in
    "The ethologic model of phonetic development: I. Phonetic contrast
    estimators" (1988).

    '''
    phonetic_count = Counter()

    for segment in word.segments:
        phonetic_count.update(classify_segment(segment))

    return reduce(operator.mul, map(lambda x: x + 1, phonetic_count.values()))


def weighted_phonetic_product(word):
    '''Given a word, compute the Phonetic Product outlined by Harold R. Bauer in
    "The ethologic model of phonetic development: I. Phonetic contrast
    estimators" (1988), using weighted values by Carterette and Jones in
    "Informal Speech: Alphabetic and Phonetic Texts with Statistical Analyses
    and Tables" (1974).

    '''
    phonetic_count = Counter()

    for segment in word.segments:
        phonetic_count.update(classify_segment(segment))

    segment_types = [phonetic_count[0] * 0.1658 + 1,
                     phonetic_count[1] * 0.3149 + 1,
                     phonetic_count[2] * 0.01129 + 1,
                     phonetic_count[3] * 0.04945 + 1,
                     phonetic_count[4] * 0.04945 + 1,
                     phonetic_count[5] * 0.18 + 1,
                     phonetic_count[6] * 0.1431 + 1,
                     phonetic_count[7] * 0.0709 + 1]

    return reduce(operator.mul, segment_types)
