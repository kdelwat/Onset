import csv
import yaml

import parse
import evolve
import deparse


def evolve_words(words, available_rules, generations=5):
    '''Evolves the given list of words according to the given list of rules, for a
    number of generations. If no more applicable rules are available, the evolution
    will stop early. Returns the evolved list of words and a list of rule which
    were applied.

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


def main():
    with open('data/features.csv', 'r') as f:
        segments = [segment for segment in csv.DictReader(f)]

    with open('data/diacritics.yaml') as f:
        diacritics = yaml.load(f)

    with open('data/rules.yaml') as f:
        rules = yaml.load(f)

    with open('data/feature-strings-with-diacritics.csv') as f:
        feature_strings = [line for line in csv.reader(f)]

    word_strings = ['mːɒtl', 'b\u02D0ɒtl']

    words = parse.parse_words(word_strings, segments, diacritics)

    evolved_words, applied_rules = evolve_words(words, rules)

    deparsed = deparse.deparse_words(evolved_words, segments, feature_strings)

    for word, evolved_word in zip(word_strings, deparsed):
        print('{0} -> {1}'.format(word, evolved_word))


if __name__ == '__main__':
    main()
