import random
import regex as re
from collections import namedtuple

# Import phoneme tables
from app.rules import PULMONIC, VOWELS

Rule = namedtuple('Rule', ['name', 'target', 'replacement', 'changes', 'environments'])

def select_rule(words, rules):
    '''Returns a sound change rule from rules applicable to the given word
    list.
    '''
    expanded_rules = expand_rule_environments(rules)
    filtered_rules = filter_rules_by_environments(words, expanded_rules)

    if len(filtered_rules) == 0:
        raise ValueError("No valid rules")
    else:
        return random.choice(filtered_rules)


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
    # Save the original environment for displaying
    environment_representation = str(environment)

    # Replace special forms
    environment = environment.replace('V', list_to_category(VOWELS.members()))
    environment = environment.replace('C', list_to_category(PULMONIC.members()))

    # Replace arbitrary categories
    for category in re.findall('{(.*)}', environment):
        if category in VOWELS:
            environment = environment.replace('{' + category + '}', list_to_category(VOWELS[category]))
        elif category in PULMONIC:
            environment = environment.replace('{' + category + '}', list_to_category(PULMONIC[category]))

    return (environment, environment_representation)


def expand_rule_environments(rules):
    '''Given a list of rules, expand special environment categories into their full
    list of phonemes. For example, the environment 'V.' might be expanded to
    '(a|e|i|o|u).'''

    expanded_rules = []

    for rule in rules:
        expanded_environments = [expand_environment(environment) for environment in rule.environments]
        expanded_rules.append(rule._replace(environments=expanded_environments))

    return expanded_rules


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
            regex = environment[0].replace('.', phonemes_match)
            targets = set(re.findall(regex, combined_words, re.MULTILINE))

            # If there are targets available, create a new rule with just those
            # targets and the current environment and add it to the filtered
            # list.
            if len(targets) != 0:
                changes = {target: replacement for target, replacement in
                           rule.changes.items() if target in targets}
                filtered_rules.append(Rule(rule.name, rule.target, rule.replacement,
                                           changes, [environment]))

    return filtered_rules
