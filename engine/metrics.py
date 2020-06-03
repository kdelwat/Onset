from collections import Counter
from functools import reduce, lru_cache
from random import random
import operator

BILABIAL = (0, {"positive": ["labial"], "negative": ["syllabic"]})
APICAL = (1, {"positive": ["coronal", "anterior"], "negative": ["syllabic"]})
PALATAL = (2, {"positive": ["distributed"], "negative": ["anterior", "syllabic"]})
VELAR = (3, {"positive": ["dorsal"], "negative": ["syllabic"]})
GLOTTAL = (4, {"negative": ["labial", "syllabic", "coronal", "dorsal"]})

FRONT = (5, {"positive": ["front"], "negative": ["back"]})
CENTRAL = (6, {"negative": ["front", "back"]})
BACK = (7, {"positive": ["back"], "negative": ["front"]})

PHONETIC_CONSTANTS = [BILABIAL, APICAL, PALATAL, VELAR, GLOTTAL, FRONT, CENTRAL, BACK]

LIQUID = {"positive": ["consonantal", "approximant"]}
RHOTIC_VOWEL = {
    "positive": ["syllabic", "coronal", "anterior", "distributed"],
    "negative": ["strident"],
}
FRICATIVE_OR_AFFRICATE = {"positive": ["delayedrelease"]}
VOICED = {"positive": ["voice"]}


@lru_cache(maxsize=None)
def classify_segment(segment):
    """Given a segment, return all phonetic constants which apply to it, in a
    list."""
    return [
        constant[0]
        for constant in PHONETIC_CONSTANTS
        if segment.meets_conditions(constant[1])
    ]


def phonetic_product(word):
    """Given a word, compute the Phonetic Product outlined by Harold R. Bauer in
    "The ethologic model of phonetic development: I. Phonetic contrast
    estimators" (1988).

    """

    # Count all applicable features in the word.
    features = []
    for segment in word.segments:
        features.extend(classify_segment(segment))

    feature_count = Counter(features)

    # Multiply the counts together, adding one to each count. The initial value
    # is one in case of words with no special features.
    return reduce(operator.mul, map(lambda x: x + 1, feature_count.values()), 1)


def weighted_phonetic_product(word):
    """Given a word, compute the Phonetic Product outlined by Harold R. Bauer in
    "The ethologic model of phonetic development: I. Phonetic contrast
    estimators" (1988), using weighted values by Carterette and Jones in
    "Informal Speech: Alphabetic and Phonetic Texts with Statistical Analyses
    and Tables" (1974).

    """

    # Count all applicable features in the word.
    features = []
    for segment in word.segments:
        features.extend(classify_segment(segment))

    feature_count = Counter(features)

    segment_types = [
        feature_count[0] * 0.1658 + 1,
        feature_count[1] * 0.3149 + 1,
        feature_count[2] * 0.01129 + 1,
        feature_count[3] * 0.04945 + 1,
        feature_count[4] * 0.04945 + 1,
        feature_count[5] * 0.18 + 1,
        feature_count[6] * 0.1431 + 1,
        feature_count[7] * 0.0709 + 1,
    ]

    return reduce(operator.mul, segment_types)


def number_of_syllables(word):
    """Given a word, compute the number of syllables it contains."""
    CV_syllable_rule = {
        "before": {"negative": ["syllabic"]},
        "conditions": {"positive": ["syllabic"]},
    }

    VC_syllable_rule = {
        "after": {"negative": ["syllabic"]},
        "conditions": {"positive": ["syllabic"]},
    }

    syllables = 0

    for index in range(len(word.segments)):
        is_CV_syllable = word.index_applicable(index, CV_syllable_rule)
        is_VC_syllable = word.index_applicable(index, VC_syllable_rule)

        if is_VC_syllable or is_CV_syllable:
            syllables += 1

    return syllables


def number_of_consonant_clusters(word):
    """Given a word, compute the number of consonant clusters it contains."""
    cluster_rule = {
        "before": {"positive": ["consonantal"]},
        "conditions": {"positive": ["consonantal"]},
        "after": {"negative": ["consonantal"]},
    }

    return len(
        [
            index
            for index in range(len(word.segments))
            if word.index_applicable(index, cluster_rule)
        ]
    )


def word_complexity_measure(word):
    """Given a word, compute the Word Complexity Measure outlined by Carol
    Stoel-Gammon in "The Word Complexity Measure: Description and application
    to developmental phonology and disorders" (2010).

    """
    WCM_score = 0

    if number_of_syllables(word) > 2:
        WCM_score += 1

    if "consonantal" in word.segments[-1].positive:
        WCM_score += 1

    WCM_score += number_of_consonant_clusters(word)

    for segment in word.segments:
        if segment.meets_conditions(VELAR[1]):
            WCM_score += 1
        elif segment.meets_conditions(LIQUID):
            WCM_score += 1
        elif segment.meets_conditions(RHOTIC_VOWEL):
            WCM_score += 1
        elif segment.meets_conditions(FRICATIVE_OR_AFFRICATE):
            WCM_score += 1
            if segment.meets_conditions(VOICED):
                WCM_score += 1

    return WCM_score


def random_value(word):
    """Given a word, return a random value."""
    return random()
