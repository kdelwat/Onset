import yaml
import sys
import os.path as path

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.join(base_directory, 'engine'))

from word import Word
from segment import Segment
from evolve import filter_rules

# Load rules
with open(path.join(base_directory, 'engine', 'data', 'rules.yaml'), 'r') as f:
    rules = yaml.load(f)


def test_filter_rules():

    rule1 = {'applies': {'positive': ['nasal']},
             'conditions': {'negative': ['nasal'],
                            'positive': ['syllabic']},
             'name': 'nasalization'}

    rule2 = {'applies': {'positive': ['tonal']},
             'conditions': {'positive': ['syllabic']},
             'name': 'valid'}

    word1 = Word([Segment(['consonantal'], ['tonal']),
                  Segment(['sonorant'], ['high'])])

    word2 = Word([Segment(['syllabic', 'low'], []),
                  Segment(['high'], ['sonorant'])])

    assert filter_rules([word1, word2], [rule1, rule2]) == [rule2]
