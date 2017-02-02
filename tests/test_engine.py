import yaml
import sys
import os.path as path

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.join(base_directory, 'engine'))

import engine


def rules_equal(first, second):
    '''Checks if two rules are equal.'''

    if first['name'] != second['name']:
        return False

    if first['description'] != second['description']:
        return False

    if set(first.get('before', {}).get('positive', [])) != set(second.get('before', {}).get('positive', [])):
        return False
    if set(first.get('before', {}).get('negative', [])) != set(second.get('before', {}).get('negative', [])):
        return False

    if set(first.get('after', {}).get('positive', [])) != set(second.get('after', {}).get('positive', [])):
        return False
    if set(first.get('after', {}).get('negative', [])) != set(second.get('after', {}).get('negative', [])):
        return False

    if set(first.get('conditions', {}).get('positive', [])) != set(second.get('conditions', {}).get('positive', [])):
        return False
    if set(first.get('conditions', {}).get('negative', [])) != set(second.get('conditions', {}).get('negative', [])):
        return False

    if set(first.get('applies', {}).get('positive', [])) != set(second.get('applies', {}).get('positive', [])):
        return False
    if set(first.get('applies', {}).get('negative', [])) != set(second.get('applies', {}).get('negative', [])):
        return False

    return True


def test_reverse_rule():

    rule = {'applies': {'positive': ['nasal']},
            'conditions': {'negative': ['nasal'],
                           'positive': ['syllabic']},
            'before': {'positive': ['nasal']},
            'name': 'nasalization',
            'description': 'A description.'}

    target = {'applies': {'negative': ['nasal']},
              'conditions': {'positive': ['syllabic', 'nasal']},
              'before': {'positive': ['nasal']},
              'name': 'nasalization',
              'description': 'A description.'}

    assert rules_equal(engine.reverse_rule(rule), target)

    rule = {'applies': {'positive': ['consonantal'],
                        'negative': ['syllabic']},
            'conditions': {'negative': ['consonantal'],
                           'positive': ['syllabic']},
            'name': 'A name',
            'description': 'A description.'}

    target = {'conditions': {'positive': ['consonantal'],
                             'negative': ['syllabic']},
              'applies': {'negative': ['consonantal'],
                          'positive': ['syllabic']},
              'name': 'A name',
              'description': 'A description.'}

    assert rules_equal(engine.reverse_rule(rule), target)

    rule = {'applies': {'positive': ['dorsal', 'high', 'front'],
                        'negative': ['low', 'back']},
            'conditions': {'negative': ['syllabic', 'dorsal']},
            'name': 'Palatalization',
            'description': 'A description.'}

    target = {'applies': {'positive': ['low', 'back'],
                          'negative': ['dorsal', 'high', 'front']},
              'conditions': {'negative': ['syllabic', 'low', 'back'],
                             'positive': ['dorsal', 'high', 'front']},
              'name': 'Palatalization',
              'description': 'A description.'}

    assert rules_equal(engine.reverse_rule(rule), target)


def test_rewrite():
    rules = [('rr', 'ɾ'), ('rl', 'ɭ'), ('rn', 'ɳ'), ('rt', 'ʈ'), ('r', 'ɻ'),
             ('ng', 'ŋ'), ('y', 'j'), ('j', 'ʒ'), ('nn', 'n'), ('aa', 'aː'),
             ('uu', 'uː'), ('ii', 'iː'), ('dd', 'x')]

    plain_word = 'buurl'
    ipa_word = 'buːɭ'

    assert engine.rewrite([plain_word], rules, to='ipa')[0] == ipa_word
    assert engine.rewrite([ipa_word], rules, to='plain')[0] == plain_word
