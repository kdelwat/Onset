import random
import re

from collections import namedtuple

# Import phoneme tables
from rules import PULMONIC, VOWELS

Rule = namedtuple('Rule', ['changes', 'environments'])


sonorization = Rule({'p': 'b', 't': 'd', 'ʈ': 'ɖ', 'c': 'ɟ', 'k': 'g', 'q': 'ɢ', 'xx': 'cc'},
                    ['^.', 'V.V', '.$', '{ubilabial}.'])

rules = [sonorization]

words = ['oxxaotatop', 'tobapɸcɒ', 'pɸxxtabasco']


def choose_rule(words, rules):
    '''Returns a sound change rule from rules applicable to the given word
    list.
    '''
    expanded_rules = expand_rule_environments(rules)
    #filtered_rules = filter_rules_by_phonemes(words, expanded_rules)
    filtered_rules = filter_rules_by_environments(words, expanded_rules)

    return filtered_rules
    # selected_rule = random.choice(filtered_rules)


def list_to_category(phonemes):
    '''Converts a list (of phoneme strings) into a single string which represents a
    regex category, i.e ['a', 'b', 'c'] becomes '(a|b|c)'.
    '''
    phonemes = [phoneme for phoneme in phonemes if phoneme != '']
    return '(?:' + '|'.join(phonemes) + ')'


def expand_environment(environment):
    '''Expand special environment categories in the given string into their full
    list of phonemes. For example, the environment 'V.V' might be expanded to
    '[aeiou].[aeiou]'. The categories V and C are special forms, for vowels and
    consonants, while other categories can be taken from the phonemes table
    using the form '{label}'.
    '''

    # Replace special forms
    environment = environment.replace('V', list_to_category(VOWELS.members()))
    environment = environment.replace('C', list_to_category(PULMONIC.members()))

    # Replace arbitrary categories
    for category in re.findall('{(.*)}', environment):
        if category in VOWELS:
            environment = environment.replace('{' + category + '}', list_to_category(VOWELS[category]))
        elif category in PULMONIC:
            environment = environment.replace('{' + category + '}', list_to_category(PULMONIC[category]))

    return environment


def expand_rule_environments(rules):
    '''Given a list of rules, expand special environment categories into their full
    list of phonemes. For example, the environment 'V.V' might be expanded to
    '[aeiou].[aeiou]'''

    expanded_rules = []

    for rule in rules:
        expanded_environments = [expand_environment(environment) for environment in rule.environments]
        expanded_rules.append(rule._replace(environments=expanded_environments))

    return expanded_rules


def intersecting(set_1, set_2):
    '''Return true if the intersection of the two sets isn't empty, false
    otherwise.
    '''
    return (len(set_1.intersection(set_2)) != 0)


def filter_rules_by_phonemes(words, rules):
    '''Returns a list of rules which contain phonemes that are in the given word
    list.
    '''
    word_phonemes = set(''.join(words))

    return [rule for rule in rules if intersecting(word_phonemes,
                                                   set(rule.changes.keys()))]


def rule_phonemes(rule):
    '''Returns a set of the target phonemes of the rule, i.e. the phonemes used as
    keys in the changes dictionary.
    '''
    return set(rule.changes.keys())


def filter_rules_by_environments(words, rules):
    '''Returns a list of rules which apply to at least one word in the given word
    list, taking into account the environments in which the rule applies. The
    rules have all extraneous phoneme pairs removed, for maximum efficiency.
    '''
    filtered_rules = []

    # Combine the word list into one string, separated by newlines, to speed up
    # regex search.
    combined_words = '\n'.join(words)

    for rule in rules:

        # Create a regex capture group from target phonemes, in the form '(a|bc|d)'.
        phonemes_match = '({0})'.format('|'.join(rule_phonemes(rule)))

        for environment in rule.environments:
            # Get a set of target phonemes which appear in the environment.
            regex = environment.replace('.', phonemes_match)
            targets = set(re.findall(regex, combined_words, re.MULTILINE))

            # If there are targets available, create a new rule with just those
            # targets and the current environment and add it to the filtered
            # list.
            if len(targets) != 0:
                changes = {target: replacement for target, replacement in
                           rule.changes.items() if target in targets}
                filtered_rules.append(Rule(changes, [environment]))

    return filtered_rules

if __name__ == '__main__':
    print(choose_rule(words, rules))

