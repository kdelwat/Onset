import yaml
import sys
import os.path as path

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.join(base_directory, 'app'))

from word import Word
from segment import Segment

# Load rules
with open(path.join(base_directory, 'app', 'data', 'rules.yaml'), 'r') as f:
    rules = yaml.load(f)


def test_overlapping_chunks():
    word = Word([])
    assert list(word.overlapping_chunks([], 3)) == []
    assert list(word.overlapping_chunks([1, 2, 3, 4, 5], 2)) == [(1, 2),
                                                                 (2, 3),
                                                                 (3, 4),
                                                                 (4, 5)]
    assert list(word.overlapping_chunks([1, 2, 3, 4, 5], 3)) == [(1, 2, 3),
                                                                 (2, 3, 4),
                                                                 (3, 4, 5)]


def test_applicable():

    rule_length_one = {'applies': {'positive': ['nasal']},
                       'conditions': {'negative': ['nasal'],
                                      'positive': ['syllabic']},
                       'name': 'nasalization'}

    rule_length_two = {'applies': {'positive': ['nasal']},
                       'before': {'positive': ['nasal']},
                       'conditions': {'negative': ['nasal'],
                                      'positive': ['syllabic']},
                       'name': 'nasalization'}

    rule_length_three = {'applies': {'positive': ['nasal']},
                         'before': {'positive': ['nasal']},
                         'after': {'negative': ['high']},
                         'conditions': {'negative': ['nasal'],
                                        'positive': ['syllabic']},
                         'name': 'nasalization'}

    applicable_word = Word([Segment(['consonantal'], ['tonal']),
                            Segment(['nasal'], ['syllabic']),
                            Segment(['syllabic'], ['nasal']),
                            Segment(['sonorant'], ['high'])])

    inapplicable_word = Word([Segment(['consonantal'], ['tonal']),
                              Segment([], ['low']),
                              Segment(['syllabic', 'nasal'], []),
                              Segment(['high'], ['sonorant'])])

    assert applicable_word.applicable(rule_length_one)
    assert applicable_word.applicable(rule_length_two)
    assert applicable_word.applicable(rule_length_three)

    assert not inapplicable_word.applicable(rule_length_one)
    assert not inapplicable_word.applicable(rule_length_two)
    assert not inapplicable_word.applicable(rule_length_three)
