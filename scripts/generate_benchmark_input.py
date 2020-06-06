# Use like python generate_benchmark_input.py n benchmark_engine_input.txt
# Generates a file containing one IPA word per line, totalling n words,
# with each word randomly generated
import csv
import sys
import os.path as path
import random

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.join(base_directory, "engine"))

MIN_WORD_LENGTH = 1
MAX_WORD_LENGTH = 10


def load_feature_strings(filename):
    """Load a feature string list from a CSV file, returning a list of
  lists where the first item in each is the IPA string and the
  second is the corresponding feature string.

  """
    with open(filename, "r") as f:
        return [line for line in csv.reader(f)]


def generate_random_word(phonemes):
    l = random.randrange(MIN_WORD_LENGTH, MAX_WORD_LENGTH + 1)

    return "".join([random.choice(phonemes) for _ in range(l)])


def main():
    n = int(sys.argv[1])
    output_filename = sys.argv[2]

    phonemes = [
        feature_string[0]
        for feature_string in load_feature_strings(
            path.join(base_directory, "engine", "data", "features.csv")
        )
    ]

    with open(output_filename, "w") as out:
        for _ in range(n):
            out.write(generate_random_word(phonemes) + "\n")


if __name__ == "__main__":
    main()
