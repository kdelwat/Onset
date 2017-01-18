import csv
import yaml

import parse
import deparse


def main():
    with open('data/features.csv', 'r') as f:
        segments = [segment for segment in csv.DictReader(f)]

    with open('data/diacritics.yaml') as f:
        diacritics = yaml.load(f)

    with open('data/feature-strings-with-diacritics.csv') as f:
        feature_strings = [line for line in csv.reader(f)]

    words = parse.parse_words(['bːɒtl', 'b\u02D0ɒtl'], segments, diacritics)
    print(deparse.deparse_words(words, segments, feature_strings))


if __name__ == '__main__':
    main()
