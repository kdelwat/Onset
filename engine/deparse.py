from typing import List

from scipy.spatial.distance import hamming

from engine.data import FeatureStrings
from engine.feature_vector import FeatureVector
from engine.word import Word


def make_matcher(feature_strings: FeatureStrings):
    possible_matches = feature_strings.items()

    # TODO: try lru_cache here
    def match_segment(target_segment: FeatureVector) -> str:
        # Best match is decided first by hamming distance, then by resulting IPA
        # length (to find the simplest sequences)
        best_match = min(
            possible_matches,
            key=lambda pm: (hamming(pm[1], target_segment), len(pm[0])),
        )

        return best_match[0]

    return match_segment


def deparse_words(words: List[Word], feature_strings: FeatureStrings):
    """Given a list of Words, return a list of IPA strings, one for each
    word."""

    matcher = make_matcher(feature_strings)

    deparsed_words = []

    for word in words:
        deparsed_words.append("".join([matcher(segment) for segment in word]))

    return deparsed_words
