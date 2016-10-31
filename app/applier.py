import random

from collections import namedtuple

Rule = namedtuple('Rule', ['changes', 'environments'])

sonorization = Rule({'p': 'b', 't': 'd', 'ʈ': 'ɖ', 'c':'ɟ', 'k': 'g', 'q': 'ɢ'},
                    ['^.', 'V.V'])

rules = [sonorization]

words = ['potato', 'tobado', 'tabasco']

def choose_rule(words, rules):
    '''Returns a sound change rule from rules applicable to the given word list.'''
    filtered_rules = filter_rules_by_phonemes(words, rules)
    # filtered_rules = filter_rules_by_environments(words, filtered_rules)

    # selected_rule = random.choice(filtered_rules)

def intersecting(set_1, set_2):
    '''Return true if the intersection of the two sets isn't empty, false
otherwise.
    '''
    return (len(set_1.intersection(set_2)) != 0)

def filter_rules_by_phonemes(words, rules):
    '''Returns a list of rules which contain phonemes that are present in the given
word list.
    '''
    word_phonemes = set(''.join(words))

    return [rule for rule in rules if intersecting(word_phonemes,
                                                   set(rule.changes.keys()))]

def filter_rules_by_environments(words, rules):
    '''Returns a list of rules which apply to at least one word in the given word
list, taking into account the environments in which the rule applies.
    '''
    pass

if __name__ == '__main__':
    choose_rule(words, rules)
