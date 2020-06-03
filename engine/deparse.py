from functools import partial, lru_cache
from Levenshtein import hamming

feature_order = [
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


@lru_cache(maxsize=None)
def feature_string(segment):
    """Convert a Segment object into a feature string."""
    feature_string = ""

    for feature in feature_order:
        if feature in segment.positive:
            feature_string += "+"
        elif feature in segment.negative:
            feature_string += "-"
        else:
            feature_string += "0"

    return feature_string


def segment_match(feature_strings, target_segment):
    """Returns the best match for the IPA string of the given Segment, from the
    given list of tuples containing feature strings. The first item in each
    tuple is the phoneme and the second is the feature string.

    """
    target_feature_string = feature_string(target_segment)

    # If the segment has previously been matched, return the cached value
    if target_feature_string in deparse_cache:
        return deparse_cache[target_feature_string]

    # Find the distance of the initial candidate to serve as a benchmark.
    best_distance = hamming(target_feature_string, feature_strings[0][1])
    best_strings = [feature_strings[0][0]]

    # Loop through the rest of the available strings. If the distance between
    # the string and the target is greater than the current best, jump to the
    # next string. Otherwise, if it's the same add it to best_strings, or if
    # it's less overwrite best_strings.
    for string in feature_strings[1:]:
        new_distance = hamming(target_feature_string, string[1])

        if new_distance > best_distance:
            continue

        elif new_distance < best_distance:
            best_distance = new_distance
            best_strings = [string[0]]

        else:
            best_strings.append(string[0])

    # Find the shortest of these strings, because we want to deparse
    # into the simplest segments possible.
    deparsed_segment = min(best_strings, key=len)

    # Add the new match to the cache.
    deparse_cache[target_feature_string] = deparsed_segment

    return deparsed_segment


def initialise_cache():
    """Creates the global cache for deparsing, where segment matches will be
    stored."""
    global deparse_cache
    deparse_cache = {}


def deparse_words(words, segments, feature_strings):
    """Given a list of Words, return a list of IPA strings, one for each
    word."""
    initialise_cache()

    # Partially apply the segment_match function to avoid repeated calls with
    # the feature_strings object.
    deparse = partial(segment_match, feature_strings)

    # Deparse each segment in each word
    word_strings = [
        "".join(deparse(segment) for segment in word.segments) for word in words
    ]

    return word_strings
