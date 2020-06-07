from functools import lru_cache, wraps
from typing import List

import numpy as np
from scipy.spatial.distance import hamming

from engine.data import FeatureStrings
from engine.feature_vector import FeatureVector
from engine.word import Word


# Use as a decorator like lru_cache, except it supports caching feature vectors as input
def fv_cache(*args, **kwargs):
    """ Modified from https://gist.github.com/Susensio/61f4fee01150caaac1e10fc5f005eb75
    """

    def decorator(function):
        @wraps(function)
        def wrapper(np_array, *args, **kwargs):
            hashable_array = tuple(np_array)
            return cached_wrapper(hashable_array, *args, **kwargs)

        @lru_cache(*args, **kwargs)
        def cached_wrapper(hashable_array, *args, **kwargs):
            array = np.array(hashable_array)
            return function(array, *args, **kwargs)

        # copy lru_cache attributes over too
        wrapper.cache_info = cached_wrapper.cache_info
        wrapper.cache_clear = cached_wrapper.cache_clear
        return wrapper

    return decorator


def make_matcher(feature_strings: FeatureStrings):
    possible_matches = feature_strings.items()

    @fv_cache(maxsize=None)
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
