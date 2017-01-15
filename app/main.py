import csv

import parser


def load_segments(filename):
    '''Load a segment feature matrix from a CSV file, returning a list of
    dictionaries with information about each segment.

    '''
    with open(filename, 'r') as f:
        return [segment for segment in csv.DictReader(f)]


def main():
    print(load_segments('data/features.csv'))


if __name__ == '__main__':
    main()
