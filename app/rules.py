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

##############################################################################
## CONSONANTS
##############################################################################
def palatalization():
    changes = {}

    for plosive in PULMONIC['plosive']:
        if plosive != '':
            changes[plosive] = plosive + 'ʲ'

    return Rule('palatalization', 'plosive', 'palatalized plosive',
                 changes,
                 ['.(?:i|y|e|ø|j)', '(?:i|y|e|ø|j).'])


def velarization():
    return Rule('velarization', 'clear l', 'dark l',
                {'l': 'ɬ'},
                ['V.', '{back}.'])


def labialization():
    changes = {}
    for phoneme in PULMONIC['plosive']:
        if phoneme != '':
            changes[phoneme] = phoneme + 'ʷ'

    return Rule('labialization', 'plosive', 'labialized plosive',
                changes,
                ['{rounded}.', '.{rounded}'])


def dentalization():
    changes = {}
    for phoneme in ['d', 't', 'n', 'r', 'ɾ']:
        changes[phoneme] = phoneme + '\u032A'

    return Rule('dentalization', 'alveolar consonant',
                'dentalized alveolar consonant',
                changes,
                ['.(?:θ|ð)'])


def rhotacism():
    return Rule('rhotacism', '[n] and [z]', '[r]',
                {'n': 'r', 'z':'r'},
                ['V.'])


def lambdacism():
    return Rule('lambdacism', '[r]', '[l]',
                {'r': 'l'},
                ['V.', '^.'])


def t_glottalization():
    return Rule('t-glottalization', '[t]', '[ʔ]',
                {'t': 'ʔ'},
                ['.C'])


##############################################################################
## CONSONANTS - LENITION
##############################################################################
def flapping():
    return Rule('flapping', '[t] and [d]', 'flap',
                {'t': 'ɾ', 'd': 'ɾ'},
                ['^.', 'V.V'])


def consonant_nasalization():
    changes = combine_lists(PULMONIC['plosive'], PULMONIC['nasal'])

    return Rule('nasalization', 'plosive', 'nasal',
                changes,
                ['V.V'])


##############################################################################
## CONSONANTS - LENITION - SONORIZATION
##############################################################################
def voicing():
    return Rule('voicing', 'unvoiced plosive', 'voiced plosive',
                {'p': 'b', 't': 'd', 'ʈ': 'ɖ', 'c': 'ɟ', 'k': 'g', 'q': 'ɢ'},
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


##############################################################################
## CONSONANTS - LENITION - OPENING
##############################################################################
def degemination():
    changes = {}
    for phoneme in PULMONIC['plosive']:
        if phoneme != '':
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
    fricatives.remove('h')
    changes = combine_lists(fricatives, ['h'] * len(fricatives))
    return Rule('dubuccalization', 'fricative', 'placeless approximant',
                changes,
                ['^.', 'V.V', '.$'])


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


##############################################################################
## CONSONANTS - FORTITION
##############################################################################
def gemination():
    changes = {}
    for phoneme in PULMONIC['plosive']:
        if phoneme != '':
            changes[phoneme] = phoneme + phoneme

    return Rule('gemination', 'plosive', 'reduplicated plosive',
                changes,
                ['V.V'])


def despirantization():
    changes = combine_lists(PULMONIC['fricative'], PULMONIC['plosive'])

    return Rule('spirantization', 'fricative', 'plosive',
                changes,
                ['^.', 'V.V'])


##############################################################################
## VOWELS
##############################################################################
def vowel_nasalization():
    changes = {}

    for vowel in VOWELS.members():
        changes[vowel] = vowel + '\u0303'

    return Rule('nasalization', 'vowel', 'nasal vowel',
                changes,
                ['{nasal}.'])

rules = [voicing(),
         palatalization(),
         velarization(),
         labialization(),
         dentalization(),
         rhotacism(),
         lambdacism(),
         degemination(),
         spirantization(),
         debuccalization(),
         gemination(),
         lateral_vocalization(),
         palatal_vocalization(),
         approximation(),
         flapping(),
         despirantization(),
         affrication(),
         deaffrication(),
         t_glottalization(),
         consonant_nasalization(),
         approximant_elision(),
         vowel_nasalization()]
