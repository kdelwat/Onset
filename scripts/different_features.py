# different_features.py
# Invoke on the command line like: python common_features.py pbtd aui
# Creates a set of features common to both groups and then outputs the
# difference between these sets.


from tabulate import tabulate
import csv
import sys
import os.path as path

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(base_directory)


def load_segments(filename):
    '''Load a segment feature matrix from a CSV file, returning a list of
    dictionaries with information about each segment.

    '''
    with open(filename, 'r') as f:
        return [segment for segment in csv.DictReader(f)]


def feature_names(filename):
    '''Load a list of available features from a given feature matrix file.

    '''
    with open(filename, 'r') as f:
        header = list(csv.reader(f))[0]
        return [feature for feature in header if feature != 'IPA']


def feature_set(segment_string):
    all_segments = load_segments(path.join(base_directory, 'engine', 'data',
                                           'features.csv'))
    target_segments = [segment for segment in all_segments if segment['IPA'] in
                       segment_string]

    common_features = {}
    for feature, value in target_segments[0].items():
        if feature != 'IPA':
            if all(segment[feature] == value for segment in target_segments):
                common_features[feature] = value

    return common_features


def main(first, second):
    first_features = feature_set(first)
    second_features = feature_set(second)

    all_features = feature_names(path.join(base_directory, 'engine', 'data',
                                           'features.csv'))

    results = []
    for feature in all_features:
        if feature in first_features and feature in second_features:
            if first_features[feature] != second_features[feature]:
                results.append([feature, first_features[feature],
                                second_features[feature]])

    print(tabulate(results, headers=['Feature', f'Group 1 ({first})', f'Group 2 ({second})']))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
