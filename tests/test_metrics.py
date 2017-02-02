import sys
import csv
import os.path as path

base_directory = path.dirname(path.dirname(path.abspath(__file__)))

sys.path.append(path.join(base_directory, 'engine'))

from metrics import phonetic_product, weighted_phonetic_product
from segment import Segment
from word import Word


def test_phonetic_product():
    word = Word([Segment(['consonantal'], ['tonal', 'long']),
                 Segment(['nasal'], ['syllabic']),
                 Segment(['syllabic', 'high', 'back'], ['nasal', 'front']),
                 Segment(['sonorant'], ['high'])])

    featureless = Word([Segment(['consonantal'], ['tonal', 'long']),
                        Segment(['nasal'], ['syllabic']),
                        Segment(['syllabic', 'high', 'back'], ['nasal']),
                        Segment(['sonorant'], ['high'])])
    assert phonetic_product(word) == 2
    assert phonetic_product(featureless) == 1
