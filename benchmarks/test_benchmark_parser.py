import os.path as path
import yaml
import sys
import csv

from engine.parse import parse_words

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.join(base_directory, "engine"))

with open(path.join(base_directory, "engine", "data", "features.csv"), "r") as f:
    segments = [segment for segment in csv.DictReader(f)]

with open(path.join(base_directory, "engine", "data", "diacritics.yaml"), "r") as f:
    diacritics = yaml.safe_load(f)
available_segments = [segment["IPA"] for segment in segments]
available_diacritics = [segment["IPA"] for segment in diacritics]


def test_parse_words(benchmark):
    word_strings = ["bæd", "bɔɪ", "bʰ\u0330k̟͡x̟"] * 10000

    benchmark(parse_words, word_strings, segments, diacritics)
