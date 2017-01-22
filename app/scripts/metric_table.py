from tabulate import tabulate
import csv
import yaml
import sys
import os.path as path

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(base_directory)

import parse
import deparse
import metrics


def main():
    target_words = ['bːɒtl', 'b\u02D0ɒtl']

    with open(path.join(base_directory, 'data', 'features.csv'), 'r') as f:
        segments = [segment for segment in csv.DictReader(f)]

    with open(path.join(base_directory, 'data', 'diacritics.yaml')) as f:
        diacritics = yaml.load(f)

    words = parse.parse_words(target_words, segments, diacritics)

    print('Metrics')
    print('===============')

    results = []
    for word, word_string in zip(words, target_words):
        results.append([word_string, metrics.phonetic_product(word)])

    print(tabulate(results, headers=['Word', 'Phonetic Product']))


if __name__ == '__main__':
    main()
