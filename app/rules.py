import random

#from app.table import Table
from table import Table

#PULMONIC = Table('app/data/pulmonic.csv')
#VOWELS = Table('app/data/vowels.csv')

PULMONIC = Table('data/pulmonic.csv')
VOWELS = Table('data/vowels.csv')

ALL_VOWELS = VOWELS['close'] + VOWELS['closeclosemid'] + VOWELS['closemid'] + VOWELS['closemidopenmid'] + VOWELS['openmid'] + VOWELS['openmidopen'] + VOWELS['open']


def in_words(search, word_list):
    '''Returns True if search string is in any of the words in word_list, else
    returns False.'''
    return any(search in word for word in word_list)


def rule(f):
    '''A decorator for all rule functions which checks to ensure rules are
    applicable to current inventory.'''
    def wrapper(*args, **kwargs):
        rules, representation = f(*args, **kwargs)

        # If the length of the rules list is 0, there are no applicable rules, so
        # return False.
        if len(rules) == 0:
            return False, None, None
        else:
            random.shuffle(rules)
            return True, rules, representation

    return wrapper


@rule
def sonorization(word_list):
    '''Implements the sonorization, or voicing, sound change, in which plosives are
    converted to their voiced equivalent.'''

    # List unvoiced plosives and their voiced equivalents
    candidates = ['p', 't', 'ʈ', 'c', 'k', 'q']
    targets = ['b', 'd', 'ɖ', 'ɟ', 'g', 'ɢ']

    available_environments = ['^_', '(V)_(V)']

    environments = [random.choice(available_environments)] * len(candidates)

    # Zip together the candidates, targets, and environments into a list of
    # rules. Include only those rules which are relevant to the given
    # inventory.
    rules = [rule for rule in zip(
        candidates, targets, environments) if in_words(rule[0], word_list)]

    representation = ['Sonorization', 'unvoiced plosive', 'voiced plosive',
                      environments[0]]

    return rules, representation


@rule
def degemination(word_list):
    '''Implements the degemination sound change, in which doubled plosives are
    converted to singular.'''

    candidates = []
    targets = []

    for phoneme in PULMONIC['plosive']:
        if phoneme != '':
            candidates.append(phoneme + phoneme)
            candidates.append(phoneme + phoneme + 'ʰ')
            targets.append(phoneme)
            targets.append(phoneme + 'ʰ')

    available_environments = ['^_', '(V)_(V)']

    environments = [random.choice(available_environments)] * len(candidates)

    # Zip together the candidates, targets, and environments into a list of
    # rules.
    rules = [rule for rule in zip(
        candidates, targets, environments) if in_words(rule[0], word_list)]

    representation = ['Degemination', 'geminated plosive', 'plosive',
                      environments[0]]

    return rules, representation


@rule
def spirantization(word_list):
    '''Implements the spirantization sound change, in which stops are converted
    to fricatives.'''

    candidates = PULMONIC['plosive']
    targets = PULMONIC['fricative']

    available_environments = ['^_', '(V)_(V)']

    environments = [random.choice(available_environments)] * len(candidates)

    # Zip together the candidates, targets, and environments into a list of
    # rules.
    rules = [rule for rule in zip(candidates, targets, environments) if in_words(rule[0], word_list) and rule[0] != '' and rule[1] != '']

    representation = ['spirantization', 'plosive', 'fricative',
                      environments[0]]

    return rules, representation


@rule
def debuccalization(word_list):
    '''Implements the debuccalization sound change, in which fricatives are
    converted to the placeless approximant.'''

    candidates = PULMONIC['fricative']
    targets = ['h'] * len(candidates)

    available_environments = ['^_', '(V)_(V)', '_$']

    environments = [random.choice(available_environments)] * len(candidates)

    # Zip together the candidates, targets, and environments into a list of
    # rules.
    rules = [rule for rule in zip(candidates, targets, environments) if in_words(rule[0], word_list)]

    representation = ['debuccalization', 'fricative', 'placeless approximant',
                      environments[0]]

    return rules, representation

@rule
def lateral_vocalization(word_list):
    '''Implements the lateral vocalization sound change, in which l is converted
    to a semivowel.'''

    candidates = []
    targets = []
    for phoneme in set(PULMONIC['lateralapproximant'] + ['ɫ']):
        if phoneme != '':
            for target in set(VOWELS['uback'] + VOWELS['rback'] + ['w', 'ɰ', 'j']):
                if target != '':
                    candidates.append(phoneme)
                    targets.append(target)

    available_environments = ['^_', '(V)_(V)', '_$']

    environments = [random.choice(available_environments)] * len(candidates)

    # Zip together the candidates, targets, and environments into a list of
    # rules.
    rules = [rule for rule in zip(candidates, targets, environments) if in_words(rule[0], word_list)]

    representation = ['vocalization', 'lateral approximant', 'semivowel/back vowel',
                      environments[0]]

    return rules, representation

@rule
def palatal_vocalization(word_list):
    '''Implements the palatal vocalization sound change, in which j is converted
    to front vowel i.'''

    available_environments = ['^_', '(V)_(V)', '_$']
    environment = random.choice(available_environments)

    representation = ['vocalization', 'palatal approximant', 'front vowel',
                      environment]

    rule = ('j', 'i', environment)
    return [rule], representation

@rule
def approximation(word_list):
    '''Implements the approximation sound change, in which continuants are
    converted to approximants.'''

    candidates = PULMONIC['fricative']
    targets = PULMONIC['approximant']

    available_environments = ['^_', '(V)_(V)', '_$']

    environment = random.choice(available_environments)

    rules = []
    for candidate, target in zip(candidates, targets):
        if candidate != '' and in_words(candidate, word_list):
            if target == '':
                rules.append((candidate, candidate + '\u031E', environment))
            else:
                rules.append((candidate, target, environment))

    representation = ['approximation', 'continuant', 'approximant',
                      environment]

    return rules, representation

@rule
def flapping(word_list):
    '''Implements the flapping sound change, in which t and d are
    converted to a tap.'''
    available_environments = ['^_', '(V)_(V)']

    environment = random.choice(available_environments)

    representation = ['flapping', '[t] and [d]', 'flap',
                      environment]

    rules = [('t', 'ɾ', environment), ('d', 'ɾ', environment)]

    return rules, representation


@rule
def affrication(word_list):
    '''Implements the affrication sound change, in which plosives are converted
    to affricates.'''

    candidates = PULMONIC['plosive'] + [p + 'ʰ' for p in PULMONIC['plosive']]
    targets = PULMONIC['nonsibilantaffricate'] + PULMONIC['nonsibilantaffricate']

    available_environments = ['(V)_(V)']

    environments = [random.choice(available_environments)] * len(candidates)

    # Zip together the candidates, targets, and environments into a list of
    # rules.
    rules = [rule for rule in zip(candidates, targets, environments) if in_words(rule[0], word_list) and rule[0] != '' and rule[1] != '']

    if in_words('t', word_list):
        rules.append(('t', 'ts', environments[0]))
    if in_words('tʰ', word_list):
        rules.append(('tʰ', 'ts', environments[0]))

    representation = ['affrication', 'plosive', 'affricate',
                      environments[0]]

    return rules, representation

@rule
def deaffrication(word_list):
    '''Implements the affrication sound change, in which plosives are converted
    to affricates.'''

    candidates = PULMONIC['nonsibilantaffricate']
    targets = PULMONIC['fricative']

    available_environments = ['(V)_(V)', '^_', '_$']

    environments = [random.choice(available_environments)] * len(candidates)

    # Zip together the candidates, targets, and environments into a list of
    # rules.
    rules = [rule for rule in zip(candidates, targets, environments) if in_words(rule[0], word_list) and rule[0] != '' and rule[1] != '']

    if in_words('ts', word_list):
        rules.append(('ts', 's', environments[0]))

    representation = ['deaffrication', 'affricate', 'fricative',
                      environments[0]]

    return rules, representation

@rule
def approximant_elision(word_list):
    '''Implements elision of approximants, in which approximants are deleted.'''

    candidates = PULMONIC['approximant']
    targets = [''] * len(candidates)

    available_environments = ['(V)_(V)', '^_', '_$']

    environments = [random.choice(available_environments)] * len(candidates)

    # Zip together the candidates, targets, and environments into a list of
    # rules.
    rules = [rule for rule in zip(candidates, targets, environments) if in_words(rule[0], word_list) and rule[0] != '']

    if in_words('h', word_list):
        rules.append(('h', '', environments[0]))
    if in_words('ɦ', word_list):
        rules.append(('ɦ', '', environments[0]))

    representation = ['elision', 'approximant', 'nothing',
                      environments[0]]

    return rules, representation

@rule
def nasalization(word_list):
    '''Implements nasalization of vowels, in which vowels are nasalized following nasal consonants.'''

    rules = []
    for candidate in PULMONIC['nasal']:
        for target in ALL_VOWELS:
            rules.append((target, target + '\u0303', candidate + '_'))

    representation = ['nasalization', 'vowel', 'nasal vowel',
                      '(nasal consonant_']

    return rules, representation
