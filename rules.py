import random

from table import Table

PULMONIC = Table('pulmonic.csv')

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
            return True, rules, representation

    return wrapper

@rule
def sonorization(inventory, word_list):
    '''Implements the sonorization, or voicing, sound change, in which plosives are
    converted to their voiced equivalent.'''

    # List unvoiced plosives and their voiced equivalents
    candidates = ['p', 't', 'ʈ', 'c', 'k', 'q']
    targets = ['b', 'd', 'ɖ', 'ɟ', 'g', 'ɢ']

    available_environments = ['^_', '(V)_(V)']

    environments = [random.choice(available_environments)] * len(candidates)

    # Zip together the candidates, targets, and environments into a list of rules.
    # Include only those rules which are relevant to the given inventory.
    rules = [rule for rule in zip(candidates, targets, environments) if rule[0] in inventory]

    representation = 'Sonorization: [unvoiced plosive]/[voiced plosive]/'+ environments[0]

    return rules, representation

@rule
def degemination(inventory, word_list):
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

    # Zip together the candidates, targets, and environments into a list of rules.
    rules = [rule for rule in zip(candidates, targets, environments) if in_words(rule[0], word_list)]

    representation = 'Degemination: [geminated plosive]/[plosive]/'+ environments[0]

    return rules, representation
