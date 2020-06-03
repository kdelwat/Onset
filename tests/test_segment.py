import sys
import os.path as path

base_directory = path.dirname(path.dirname(path.abspath(__file__)))

sys.path.append(path.join(base_directory, "engine"))

from engine.segment import Segment


def test_initialisation():
    feature_dictionary = {"stress": "+", "long": "-", "continuant": "0", "IPA": "b"}

    segment = Segment.from_dictionary(feature_dictionary)

    assert segment.positive == ["stress"]
    assert segment.negative == ["long"]


def test_setters():
    feature_dictionary = {"stress": "+", "long": "-", "continuant": "0", "IPA": "b"}

    segment = Segment.from_dictionary(feature_dictionary)

    segment.add_positive("long")
    assert segment.positive == ["stress", "long"]
    assert segment.negative == []

    segment.add_negative("stress")
    assert segment.positive == ["long"]
    assert segment.negative == ["stress"]

    segment.add_negative("stress")
    assert segment.positive == ["long"]
    assert segment.negative == ["stress"]


def test_addition():
    feature_dictionary = {"stress": "+", "syllabic": "-", "continuant": "0", "IPA": "b"}

    segment = Segment.from_dictionary(feature_dictionary)

    syllabic_diacritic = Segment(["syllabic"], ["voice"])

    addition = segment + syllabic_diacritic
    assert addition.positive == ["stress", "syllabic"]
    assert addition.negative == ["voice"]


def test_meets_conditions():
    segment = Segment(["syllabic", "voice"], ["consonantal", "continuant"])

    assert segment.meets_conditions({})
    assert segment.meets_conditions({"positive": ["syllabic"]})
    assert segment.meets_conditions(
        {"positive": ["syllabic", "voice"], "negative": ["continuant"]}
    )
    assert not segment.meets_conditions(
        {"positive": ["lateral"], "negative": ["continuant"]}
    )
