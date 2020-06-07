import sys

import numpy as np
import os.path as path

from engine.data import (
    feature_string_to_feature_vector,
    load_segments,
    load_diacritics,
    load_feature_strings,
)
from engine.feature_vector import fv_show

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.join(base_directory, "engine"))

from engine.parse import token_to_segment, parse_words
from engine.deparse import deparse_words


def test_token_to_segment():
    cases = [
        ["b", "---+-------+--+---000--00000"],
        ["b\u0325", "---+----------+---000--00000"],
        ["bː", "--++-------+--+---000--00000"],
        ["bː\u0303", "--++------++--+---000--00000"],
    ]

    segments = load_segments()
    diacritics = load_diacritics()

    for case in cases:
        want = feature_string_to_feature_vector(case[1])
        got = token_to_segment(case[0], segments, diacritics)

        assert np.array_equal(
            got, want
        ), f"Error parsing token {case[0]} to segment: want {case[1]}, got {fv_show(got)}"


def test_parse_words():
    segments = load_segments()
    diacritics = load_diacritics()

    word_strings = ["bædk̟͡x̟", "bɔɪ"]
    words = parse_words(word_strings, segments, diacritics)

    assert len(words) == 2
    assert all([isinstance(word, np.ndarray) for word in words])


def test_parse_deparse():
    word_strings = ["bæd", "bɔɪ", "b\u02D0ɒtl"]

    segments = load_segments()
    diacritics = load_diacritics()
    feature_strings = load_feature_strings()

    words = parse_words(word_strings, segments, diacritics)

    assert deparse_words(words, feature_strings) == word_strings
