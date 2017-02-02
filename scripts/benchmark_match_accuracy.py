from tabulate import tabulate
import csv
import yaml
import sys
import os.path as path

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.join(base_directory, 'engine'))

import deparse
from segment import Segment


def load_segments(filename):
    '''Load a segment feature matrix from a CSV file, returning a list of
    dictionaries with information about each segment.

    '''
    with open(filename, 'r') as f:
        return [segment for segment in csv.DictReader(f)]


def load_feature_strings(filename):
    '''Load a feature string list from a CSV file, returning a list of
    lists where the first item in each is the IPA string and the
    second is the corresponding feature string.

    '''
    with open(filename, 'r') as f:
        return [line for line in csv.reader(f)]


def load_diacritics(filename):
    '''Load diacritic data from a YAML file, returning a list of
    dictionaries with information about each diacritic.

    '''
    with open(filename, 'r') as f:
        return yaml.load(f)


def main():
    segments = load_segments(path.join(base_directory, 'engine', 'data', 'features.csv'))
    diacritics = load_diacritics(path.join(base_directory, 'engine', 'data', 'diacritics.yaml'))

    datasets = ['feature-strings', 'hayes-feature-strings',
                'feature-strings-with-diacritics']

    print('Beginning benchmark\n===================\n')

    results = []

    for dataset in datasets:
        print('Running dataset: {0}'.format(dataset))
        filename = '{0}.csv'.format(dataset)

        accuracy = benchmark_match_accuracy(segments, diacritics, filename)

        results.append([dataset, accuracy])

    print('Finished!\n')
    print(tabulate(results, headers=['Dataset', 'Accuracy']))


def benchmark_match_accuracy(segments, diacritics, filename):
    '''Convert all given segments to feature strings, then convert back to
    segments. Use the given feature string file. Return the percentage accuracy
    of the conversion.

    '''
    feature_strings = load_feature_strings(path.join(base_directory, 'engine',
                                                     'data', filename))

    matches = []

    deparse.initialise_cache()

    for segment in segments:
        base_segment = Segment.from_dictionary(segment)
        matches.append((segment['IPA'],
                        deparse.segment_match(feature_strings, base_segment)))

        for diacritic in diacritics:
            IPA_representation = segment['IPA'] + diacritic['IPA']

            if base_segment.meets_conditions(diacritic['conditions']):
                diacritic_segment = base_segment + Segment(diacritic['applies'].get('positive', []),
                                                           diacritic['applies'].get('negative', []))

                matches.append((IPA_representation,
                                deparse.segment_match(feature_strings,
                                                      diacritic_segment)))

    successes = len([match for match in matches if match[0] == match[1]])

    return (successes / len(matches))


if __name__ == '__main__':
    main()
