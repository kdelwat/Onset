import yaml
import sys
import os.path as path

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.join(base_directory, 'engine'))

from word import Word
from segment import Segment

# Load rules
with open(path.join(base_directory, 'engine', 'data', 'rules.yaml'), 'r') as f:
    rules = yaml.load(f)


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


def test_apply_rule():
    rule = {'applies': {'positive': ['nasal']},
            'conditions': {'negative': ['nasal'],
                           'positive': ['syllabic']},
            'name': 'nasalization'}

    word = Word([Segment(['nasal'], ['syllabic']),
                 Segment(['syllabic'], ['nasal'])])

    target_word = Word([Segment(['nasal'], ['syllabic']),
                        Segment(['syllabic', 'nasal'], [])])

    assert word.apply_rule(rule) == target_word


def test_equality():
    word1 = Word([Segment(['nasal'], ['syllabic']),
                  Segment(['syllabic'], ['nasal'])])

    word2 = Word([Segment(['nasal'], ['syllabic']),
                  Segment(['syllabic'], ['nasal'])])

    assert word1 == word2


def test_index_applicable():
    syllable_rule = {'before': {'negative': ['syllabic']},
                     'conditions': {'positive': ['syllabic']}}

    word = Word([Segment(['consonantal', 'voice', 'labial', 'long'],
                         ['syllabic', 'stress']),
                 Segment(['syllabic', 'sonorant', 'continuant', 'approximant', 'voice', 'labial', 'round', 'dorsal', 'low', 'back'],
                         ['stress', 'long']),
                 Segment(['consonantal', 'coronal', 'anterior'],
                         ['syllabic', 'stress'])])

    assert word.index_applicable(1, syllable_rule)
