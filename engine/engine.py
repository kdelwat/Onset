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


def run_engine(words, generations=5, rewrite_rules=[], reverse=False,
               metric=metrics.phonetic_product, optimisation_function=min):
    '''Evolves the language specified by a list of word strings according to
    parameters:

        generations: the maximum number of rules to apply during evolution.
        rewrite_rules: a list of rewrite tuples in form (plain, ipa) which
                       is used to transcribe the input words from orthographic
                       representation to IPA.
        reverse: if true, evolution will run in reverse.
        metric: the metric function that will be used in selecting rules.
        optimisation_function: the function that will determine the best
                               metric result to use during selection. Should
                               be either min or max.

    Returns a list of evolved word strings and a list of applied rules.

    '''

    # Parse the word strings into Word objects
    parsed_words = parse.parse_words(words, segments, diacritics)

    # Evolve the words for the given number of generations
    evolved_words, applied_rules = evolve_words(parsed_words, rules,
                                                generations)

    # Deparse the evolved words into strings
    deparsed_words = deparse.deparse_words(evolved_words, segments,
                                           feature_strings)

    return deparsed_words, applied_rules


def evolve_words(words, available_rules, generations):
    '''Evolves the given list of words according to the given list of rules, for a
    number of generations. If no more applicable rules are available, the
    evolution will stop early. Returns the evolved list of words and a list of
    rule which were applied.

    '''
    applied_rules = []

    try:
        for _ in range(generations):
            rule, words = evolve.evolve(words, available_rules)
            applied_rules.append(rule)

    # StopIteration is raised when there are no more applicable rules
    except StopIteration:
        return words, applied_rules

    return words, applied_rules
