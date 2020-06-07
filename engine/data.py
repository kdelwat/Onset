import csv
from typing import Dict, Union, Hashable, Any, OrderedDict, List

import numpy as np
import yaml
import sys
import os.path as path

from engine.feature_vector import FeatureVector

YAML = Union[Dict[Hashable, Any], list, None]
Segments = Dict[str, FeatureVector]
Diacritics = Dict[str, FeatureVector]
FeatureStrings = Dict[str, FeatureVector]

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.join(base_directory, "engine"))

FEATURES = [
    "syllabic",
    "stress",
    "long",
    "consonantal",
    "sonorant",
    "continuant",
    "delayedrelease",
    "approximant",
    "tap",
    "trill",
    "nasal",
    "voice",
    "spreadglottis",
    "constrictedglottis",
    "labial",
    "round",
    "labiodental",
    "coronal",
    "anterior",
    "distributed",
    "strident",
    "lateral",
    "dorsal",
    "high",
    "low",
    "front",
    "back",
    "tense",
]


def segment_to_feature_vector(segment) -> FeatureVector:
    feature_values = []
    for feature in FEATURES:
        if segment[feature] == "+":
            feature_values.append(1)
        elif segment[feature] == "-":
            feature_values.append(-1)
        else:
            feature_values.append(0)

    return np.array(feature_values, dtype=np.int8)


def diacritic_to_feature_vector(diacritic) -> FeatureVector:
    feature_values = []
    for feature in FEATURES:
        if feature in diacritic["applies"].get("positive", []):
            feature_values.append(1)
        elif feature in diacritic["applies"].get("negative", []):
            feature_values.append(-1)
        else:
            feature_values.append(0)

    return np.array(feature_values, dtype=np.int8)


def feature_string_to_feature_vector(fs: str) -> FeatureVector:
    feature_values = []
    for feature in fs:
        if feature == "+":
            feature_values.append(1)
        elif feature == "-":
            feature_values.append(-1)
        else:
            feature_values.append(0)

    return np.array(feature_values, dtype=np.int8)


def load_yaml(filename: str) -> YAML:
    p = path.join(base_directory, "engine", "data", f"{filename}.yaml")

    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_csv(filename: str) -> List[OrderedDict[str, str]]:
    p = path.join(base_directory, "engine", "data", f"{filename}.csv")

    with open(p, "r", encoding="utf-8") as f:
        return [row for row in csv.DictReader(f)]


def load_segments() -> Segments:
    return {s["IPA"]: segment_to_feature_vector(s) for s in load_csv("features")}


def load_diacritics() -> Diacritics:
    return {d["IPA"]: diacritic_to_feature_vector(d) for d in load_yaml("diacritics")}


def load_rules():
    return load_yaml("rules")


def load_feature_strings() -> FeatureStrings:
    return {
        f["IPA"]: feature_string_to_feature_vector(f["feature_string"])
        for f in load_csv("feature-strings")
    }
