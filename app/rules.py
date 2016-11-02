import random

from app.table import Table
from collections import namedtuple

PULMONIC = Table('app/data/pulmonic.csv')
VOWELS = Table('app/data/vowels.csv')

# A Rule is a namedtuple with the following fields:
#     name: a string representing the process' name
#     target: a string representing the process' target
#     replacement: a string representing the process' replacement
#     changes: a dictionary of sound changes
#     environments: a list of environments to apply the rule to
Rule = namedtuple('Rule', ['name', 'target', 'replacement', 'changes', 'environments'])


def combine_lists(list_1, list_2):
    '''Combines two lists into a dictionary, ensuring that any pair that contains a
    '' is removed.
    '''
    pairs = [pair for pair in zip(list_1, list_2) if pair[0] != '' and pair[1] != '']
    return dict(pairs)


def in_words(search, word_list):
    '''Returns True if search string is in any of the words in word_list, else
    returns False.'''
    return any(search in word for word in word_list)


def rule(f):
    '''A decorator for all rule functions which checks to ensure rules are
    applicable to current inventory.'''
    def wrapper(*args, **kwargs):
        rules, representation = f(*args, **kwargs)

        # If the length of the rules list is 0, there are no applicable rules,
        # so return False.
        if len(rules) == 0:
            return False, None, None
        else:
            random.shuffle(rules)
            return True, rules, representation

    return wrapper


def sonorization():
    return Rule('sonorization', 'unvoiced plosive', 'voiced plosive',
                {'p': 'b', 't': 'd', 'ʈ': 'ɖ', 'c': 'ɟ', 'k': 'g', 'q': 'ɢ'},
                ['^.', 'V.V', '.$'])


def degemination():
    changes = {}
    for phoneme in PULMONIC['plosive']:
        changes[phoneme + phoneme] = phoneme
        changes[phoneme + phoneme + 'ʰ'] = phoneme + 'ʰ'

    return Rule('degemination', 'geminated plosive', 'plosive',
                changes,
                ['^.', 'V.V'])


def spirantization():
    changes = combine_lists(PULMONIC['plosive'], PULMONIC['fricative'])

    return Rule('spirantization', 'plosive', 'fricative',
                changes,
                ['^.', 'V.V'])


def debuccalization():
    fricatives = PULMONIC['fricative']
    changes = combine_lists(fricatives, ['h'] * len(fricatives))
    return Rule('dubuccalization', 'fricative', 'placeless approximant',
                changes,
                ['^.', 'V.V', '.$'])


def lateral_vocalization():
    return Rule('vocalization', 'lateral approximant', 'semivowel',
                {'l': 'j', 'ɫ': 'w'},
                ['^.', 'V.V', '.$'])


def palatal_vocalization():
    return Rule('vocalization', 'palatal approximant', 'front vowel',
                {'j': 'i'},
                ['^.', 'V.V', '.$'])


def approximation():
    changes = {}

    for fricative, approximant in zip(PULMONIC['fricative'], PULMONIC['approximant']):
        if fricative != '':
            if approximant == '':
                changes[fricative] = fricative + '\u031E'
            else:
                changes[fricative] = approximant

    return Rule('approximation', 'continuant', 'approximant',
                changes,
                ['^.', 'V.V', '.$'])


def flapping():
    return Rule('flapping', '[t] and [d]', 'flap',
                {'t': 'ɾ', 'd': 'ɾ'},
                ['^.', 'V.V'])


def affrication():
    changes = {}

    for plosive, affricate in zip(PULMONIC['plosive'], PULMONIC['nonsibilantaffricate']):
        if plosive != '' and affricate != '':
            changes[plosive] = affricate
            changes[plosive + 'ʰ'] = affricate

    changes['t'] = 'ts'
    changes['tʰ'] = 'ts'

    return Rule('affrication', 'plosive', 'affricate',
                changes,
                ['V.V'])


def deaffrication():
    changes = combine_lists(PULMONIC['nonsibilantaffricate'], PULMONIC['fricative'])
    changes['ts'] = 's'

    return Rule('deaffrication', 'affricate', 'fricative',
                changes,
                ['^.', 'V.V', '.$'])


def approximant_elision():
    changes = {}

    for approximant in PULMONIC['approximant']:
        if approximant != '':
            changes[approximant] = ''

    changes['h'] = ''
    changes['ɦ'] = ''

    return Rule('elision', 'approximant', 'nothing',
                changes,
                ['^.', 'V.V', '.$'])


def nasalization():
    changes = {}

    for vowel in VOWELS.members():
        changes[vowel] = vowel + '\u0303'

    return Rule('nasalization', 'vowel', 'nasal vowel',
                changes,
                '{nasal}.')

rules = [sonorization(),
         degemination(),
         spirantization(),
         debuccalization(),
         lateral_vocalization(),
         palatal_vocalization(),
         approximation(),
         flapping(),
         affrication(),
         deaffrication(),
         approximant_elision()]
