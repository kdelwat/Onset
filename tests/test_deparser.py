import sys
import csv
import os.path as path

base_directory = path.dirname(path.dirname(path.abspath(__file__)))

sys.path.append(path.join(base_directory, "engine"))

from engine.deparse import feature_string
from engine.segment import Segment


def test_feature_string():
    segment = Segment(
        ["consonantal", "voice", "labial"],
        [
            "syllabic",
            "stress",
            "long",
            "sonorant",
            "continuant",
            "delayedrelease",
            "approximant",
            "tap",
            "trill",
            "nasal",
            "spreadglottis",
            "constrictedglottis",
            "round",
            "labiodental",
            "coronal",
            "lateral",
            "dorsal",
        ],
    )

    assert feature_string(segment) == "---+-------+--+---000--00000"
