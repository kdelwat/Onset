import csv
import yaml
import sys
import os.path as path

import parse
import deparse
import evolve
import metrics

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.join(base_directory, 'engine'))

segments_path = path.join(base_directory, 'engine', 'data', 'features.csv')
with open(segments_path, 'r') as f:
    segments = [segment for segment in csv.DictReader(f)]

diacritics_path = path.join(base_directory, 'engine', 'data', 'diacritics.yaml')
with open(diacritics_path, 'r') as f:
    diacritics = yaml.load(f)

rules_path = path.join(base_directory, 'engine', 'data', 'rules.yaml')
with open(rules_path, 'r') as f:
    rules = yaml.load(f)

feature_strings_path = path.join(base_directory, 'engine', 'data',
                                 'feature-strings-with-diacritics.csv')
with open(feature_strings_path, 'r') as f:
    feature_strings = [line for line in csv.reader(f)]


def rewrite(words, rules, to='ipa'):
    '''Rewrite a list of words according to a list of tuple rules of form
    (plain, ipa), in direction given by target.'''
    if len(rules) == 0:
        return words

    if to == 'ipa':
        return [word.replace(rule[0], rule[1]) for rule in rules
                for word in words]

    elif to == 'plain':
        return [word.replace(rule[1], rule[0]) for rule in rules
                for word in words]


def run_engine(words, generations=5, rewrite_rules=[], reverse=False,
               metric=metrics.phonetic_product, optimisation_function=min):
    '''Evolves the language specified by a list of word strings according to
    parameters:

        generations: the maximum number of rules to apply during evolution.
        rewrite_rules: a list of rewrite tuples in form (plain, ipa) which
                       is used to transcribe the input words from orthographic
                       representation to IPA.
        reverse: if True, run the evolution in reverse.
        metric: the metric function that will be used in selecting rules.
        optimisation_function: the function that will determine the best
                               metric result to use during selection. Should
                               be either min or max.

    Returns a list of evolved word strings and a list of applied rules.

    '''
    # Apply the given transcription rules
    words = rewrite(words, rewrite_rules, to='ipa')

    # Parse the word strings into Word objects
    parsed_words = parse.parse_words(words, segments, diacritics)

    if reverse:
        evolution_function = evolve_words_reverse
    else:
        evolution_function = evolve_words

    # Evolve the words for the given number of generations
    evolved_words, applied_rules = evolution_function(parsed_words, rules,
                                                      generations, metric,
                                                      optimisation_function)

    # Deparse the evolved words into strings
    deparsed_words = deparse.deparse_words(evolved_words, segments,
                                           feature_strings)

    # Convert back to orthographic representation using the given transcription
    # rules
    deparsed_words = rewrite(deparsed_words, rewrite_rules, to='plain')

    return deparsed_words, applied_rules


def evolve_words(words, available_rules, generations, metric,
                 optimisation_function):
    '''Evolves the given list of words according to the given list of rules, for a
    number of generations. If no more applicable rules are available, the
    evolution will stop early. Returns the evolved list of words and a list of
    rule which were applied.

    '''
    applied_rules = []

    try:
        for _ in range(generations):
            rule, words = evolve.evolve(words, available_rules, metric,
                                        optimisation_function)
            applied_rules.append(rule)

    # StopIteration is raised when there are no more applicable rules
    except StopIteration:
        return words, applied_rules

    return words, applied_rules


def evolve_words_reverse(words, available_rules, generations, metric,
                         optimisation_function):
    '''Evolves the given list of words in reverse, according to the given list of
    rules, for a number of generations. If no more applicable rules are
    available, the evolution will stop early. Returns the evolved list of words
    and a list of rule which were applied.

    '''
    # Transform each rule to its reversed equivalent
    reverse_rules = map(reverse_rule, available_rules)

    # Invert the optimisation algorithm
    if optimisation_function == min:
        optimisation_function = max
    else:
        optimisation_function = min

    applied_rules = []

    try:
        for _ in range(generations):
            rule, words = evolve.evolve(words, reverse_rules, metric,
                                        optimisation_function)
            applied_rules.append(rule)

    # StopIteration is raised when there are no more applicable rules
    except StopIteration:
        return words, applied_rules

    return words, applied_rules


def reverse_rule(rule):
    '''Given a rule dictionary, transform it so that it applies the rule in
    reverse.'''
    reversed_rule = {'name': rule['name'], 'description': rule['description']}

    # Before and after conditions are unchanged
    if 'before' in rule:
        reversed_rule['before'] = rule['before']
    if 'after' in rule:
        reversed_rule['after'] = rule['after']

    # Invert application
    new_applies = {}
    if 'positive' in rule['applies']:
        new_applies['negative'] = list(set(rule['applies']['positive']))

    if 'negative' in rule['applies']:
        new_applies['positive'] = list(set(rule['applies']['negative']))

    # The new conditions are the same as the old application features.
    # We must use a deep copy to prevent in-place modification.
    new_conditions = copy.deepcopy(rule['applies'])

    # Construct set containing all features present in the new conditions.
    new_conditions_set = set(new_conditions.get('positive', []) +
                             new_conditions.get('negative', []))

    # For each feature in the old conditions, if it isn't in the new conditions
    # add it, keeping the same polarity. This catches conditions that aren't
    # changed by the rule.
    for feature in rule['conditions'].get('positive', []):
        if feature not in new_conditions_set:
            if 'positive' in new_conditions:
                new_conditions['positive'].append(feature)
            else:
                new_conditions['positive'] = [feature]
    for feature in rule['conditions'].get('negative', []):
        if feature not in new_conditions_set:
            if 'negative' in new_conditions:
                new_conditions['negative'].append(feature)
            else:
                new_conditions['negative'] = [feature]

    reversed_rule['conditions'] = new_conditions
    reversed_rule['applies'] = new_applies

    return reversed_rule


def apply_rules(words, rules, rewrite_rules=[]):
    '''Given a list of word strings and a list of rules, apply each rule to the
    words and return the new word strings.'''

    # Apply the given transcription rules
    words = rewrite(words, rewrite_rules, to='ipa')

    # Parse the word strings into Word objects
    parsed_words = parse.parse_words(words, segments, diacritics)

    # Apply each rule in sequence
    for rule in rules:
        parsed_words = [word.apply_rule(rule) for word in parsed_words]

    # Deparse the evolved words into strings
    deparsed_words = deparse.deparse_words(parsed_words, segments,
                                           feature_strings)

    # Convert back to orthographic representation using the given transcription
    # rules
    deparsed_words = rewrite(deparsed_words, rewrite_rules, to='plain')

    return deparsed_words
