import random
import re
from itertools import takewhile
from pprint import pprint

import rules
from table import Table

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
    #rules = load_rules('rules.txt')
    inventory = Table('pulmonicinventory.csv')
    pprint(rules.sonorization(inventory))
    pprint(rules.degemination(inventory))

if __name__ == '__main__':
    main()

