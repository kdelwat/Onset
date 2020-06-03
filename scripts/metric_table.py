from tabulate import tabulate
import csv
import yaml
import sys
import os.path as path

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.join(base_directory, "engine"))

import engine.parse as parse
import engine.metrics as metrics


def main():
    target_words = ["aba", "bːɒtl", "b\u02D0ɒtl", "b\u02D0ɒbtdolie"]

    with open(path.join(base_directory, "engine", "data", "features.csv"), "r") as f:
        segments = [segment for segment in csv.DictReader(f)]

    with open(path.join(base_directory, "engine", "data", "diacritics.yaml")) as f:
        diacritics = yaml.safe_load(f)

    words = parse.parse_words(target_words, segments, diacritics)

    print("Metrics")
    print("===============")

    results = []
    for word, word_string in zip(words, target_words):
        results.append(
            [
                word_string,
                metrics.phonetic_product(word),
                metrics.weighted_phonetic_product(word),
                metrics.number_of_syllables(word),
                metrics.number_of_consonant_clusters(word),
                metrics.word_complexity_measure(word),
            ]
        )

    print(
        tabulate(
            results,
            headers=[
                "Word",
                "Phonetic Product",
                "Weighted Phonetic Product",
                "Syllables",
                "Consonant Clusters",
                "WCM",
            ],
        )
    )


if __name__ == "__main__":
    main()
