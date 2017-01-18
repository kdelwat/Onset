# feature_string_collisions.py
# This script loads the segment and diacritic feature data. For each segment,
# it creates a feature string, then counts and outputs duplicate feature strings.
#
# Next, it does the same but combines each segment with all compatible diacritics.
#
# The script is useful in diagnosing collision errors with the deparser.

import csv
import yaml

from collections import Counter

import sys
import os.path as path

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(base_directory)

import deparse
from segment import Segment


def load_segments(filename):
    '''Load a segment feature matrix from a CSV file, returning a list of
    dictionaries with information about each segment.

    '''
    with open(filename, 'r') as f:
        return [segment for segment in csv.DictReader(f)]


def print_duplicates(list_of_tuples):
    feature_strings = [x[1] for x in list_of_tuples]
    duplicate_strings = [string for string, count in Counter(feature_strings).items() if count > 1]

    print('There were {0} duplicates:'.format(len(duplicate_strings)))

    for string in duplicate_strings:
        shared_ipa = [x[0] for x in list_of_tuples if x[1] == string]
        print('\tMatch: {0}'.format(' '.join(shared_ipa)))


def main():
    segments = load_segments(path.join(base_directory, 'data', 'features.csv'))

    with open(path.join(base_directory, 'data', 'diacritics.yaml')) as f:
        diacritics = yaml.load(f)

    print('Generating basic feature strings')
    print('================================')
    feature_strings = []

    for segment in segments:
        base_segment = Segment.from_dictionary(segment)
        feature_strings.append((segment['IPA'], deparse.feature_string(base_segment)))

    print('\nGenerated {0} feature strings'.format(len(feature_strings)))
    print_duplicates(feature_strings)

    print('\nGenerating diacritic feature strings')
    print('================================')
    feature_strings = []

    for segment in segments:
        base_segment = Segment.from_dictionary(segment)
        feature_strings.append((segment['IPA'],
                                deparse.feature_string(base_segment)))

        for diacritic in diacritics:
            IPA_representation = segment['IPA'] + diacritic['symbol']

            if base_segment.meets_conditions(diacritic['conditions']):
                diacritic_segment = base_segment + Segment(diacritic['applies'].get('positive', []),
                                                           diacritic['applies'].get('negative', []))
                feature_strings.append((IPA_representation,
                                        deparse.feature_string(diacritic_segment)))

    print('\nGenerated {0} feature strings'.format(len(feature_strings)))
    print_duplicates(feature_strings)

if __name__ == '__main__':
    main()
