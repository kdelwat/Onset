import random
import re
from itertools import takewhile
from pprint import pprint

from table import Table

PULMONIC = Table('pulmonic.csv')

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
def sonorization(inventory):
    '''Implements the sonorization, or voicing, sound change, in which plosives are
    converted to their voiced equivalent.'''

    # List unvoiced plosives and their voiced equivalents
    candidates = ['p', 't', 'ʈ', 'c', 'k', 'q']
    targets = ['b', 'd', 'ɖ', 'ɟ', 'g', 'ɢ']

    available_environments = ['^_', 'V_V']

    environments = [random.choice(available_environments)] * len(candidates)

    # Zip together the candidates, targets, and environments into a list of rules.
    # Include only those rules which are relevant to the given inventory.
    rules = [rule for rule in zip(candidates, targets, environments) if rule[0] in inventory]

    representation = 'Sonorization: [unvoiced plosive]/[voiced plosive]/'+ environments[0]

    return rules, representation

@rule
def degemination(inventory):
    '''Implements the degemination sound change, in which doubled plosives are
    converted to singular.'''

    candidates = []
    targets = []

    for phoneme in PULMONIC['plosive']:
        candidates.append(phoneme + phoneme)
        candidates.append(phoneme + phoneme + 'ʰ')
        targets.append(phoneme)
        targets.append(phoneme + 'ʰ')

    available_environments = ['^_', 'V_V']

    environments = [random.choice(available_environments)] * len(candidates)

    # Zip together the candidates, targets, and environments into a list of rules.
    rules = [rule for rule in zip(candidates, targets, environments)]

    representation = 'Degemination: [geminated plosive]/[plosive]/'+ environments[0]

    return rules, representation

def load_rules(filename):
    '''Loads a list of rules, in the following format:

    [label1]
    x:y
    z:a

    [label2]
    b:c

    which would become:

    {'label1': (x, y) ..., 'label2': (b,c)}'''

    # Read stripped, non-blank lines into list
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip() != '']

    # Iterate through list, splitting on labels
    rules_list = []
    current_rule = [lines[0][1:-1]]

    for item in lines[1:]:
        if item[0] == '[':
            rules_list.append(current_rule)
            current_rule = [item[1:-1]]
        else:
            current_rule.append(tuple(item.split(':')))
    rules_list.append(current_rule)

    # Convert rule list to dictionary
    rules = {}
    for rule in rules_list:
        rules[rule[0]] = rule[1:]

    return rules

def apply_rule(word, rule):
    '''Applies rule in the form (target, replacement, environment) to the word.
    Environment is in the form of string like 'a_c', where the underscore is
    taken by the target and replacement.'''
    target, replacement, environment = rule

    # Create target and replacement strings
    target_string = environment.replace('_', target)
    replacement_string = environment.replace('_', replacement)

    # Delete special characters from replacement string that may be present
    # in the environment
    if replacement_string[0] == '^':
        replacement_string = replacement_string[1:]
    if replacement_string[-1] == '$':
        replacement_string = replacement_string[:-1]

    # Return the modified word
    return re.sub(target_string, replacement_string, word)

def main():
    rules = load_rules('rules.txt')
    inventory = Table('pulmonicinventory.csv')
    pprint(sonorization(inventory))
    pprint(degemination(inventory))

if __name__ == '__main__':
    main()

