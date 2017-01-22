# common_features.py
# Invoke on the command line like: python common_features.py pbtd
# Outputs all features common to all of the given segments, to help
# in rule writing.

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


def main(segment_string):
    all_segments = load_segments(path.join(base_directory, 'data',
                                           'features.csv'))
    target_segments = [segment for segment in all_segments if segment['IPA'] in
                       segment_string]

    common_features = []
    for feature, value in target_segments[0].items():
        if feature != 'IPA' and value != '0':
            if all(segment[feature] == value for segment in target_segments):
                common_features.append([feature, value])

    print('Common features')
    print('===============')
    print(tabulate(common_features, headers=['Feature', 'Value']))


if __name__ == '__main__':
    main(sys.argv[1])
