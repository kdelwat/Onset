from engine.segment import Segment
from engine.word import Word

import re


# Construct a regex to match an IPA segment.
#
# The regex will match a phoneme, zero or more diacritics, and then optionally a phoneme and diacritics joined with the
# Unicode overhead combining mark (which captures digraphs).
#
# Precompiling the regex once allows us to match in O(n) time.
def create_segment_regex(segments, diacritics):
    all_segments = "".join([segment for segment in segments if len(segment) == 1])
    all_diacritics = "".join(diacritics)

    return re.compile(
        f"[{all_segments}][{all_diacritics}]*(?:\u0361[{all_segments}][{all_diacritics}])?"
    )


def parse_words(strings, segments, diacritics):
    """Given a list of word strings (in IPA), return a list of Word objects
    containing parsed segments. Use the given list of segment dictionaries and
    diacritic rules.

    """

    r = create_segment_regex(
        [segment["IPA"] for segment in segments],
        [diacritic["IPA"] for diacritic in diacritics],
    )

    words = []

    for word in strings:
        try:
            tokens = r.findall(word)
        except ValueError as subword:
            error = (
                "Error parsing word: {0}. There was an unknown character "
                "in the subword: {1}"
            )
            raise ValueError(error.format(word, subword))

        parsed_segments = [
            token_to_segment(token, segments, diacritics) for token in tokens
        ]
        words.append(Word(parsed_segments))

    return words


def find_segment(string, segment_strings):
    """Search the segment dictionary for the segment with the correct IPA
    string."""
    return [segment for segment in segment_strings if segment["IPA"] == string][0]


def token_to_segment(token, segment_list, diacritic_list):
    """Converts a string token in IPA to Segment object, given
    a list of dictionaries representing segments and the same representing
    diacritics."""

    diacritic_strings = [segment["IPA"] for segment in diacritic_list]

    # Isolate the base IPA segment string
    base_string = "".join(filter(lambda x: x not in diacritic_strings, token))

    # Isolate an iterable of diacritics present
    diacritics = [
        diacritic for diacritic in diacritic_list if diacritic["IPA"] in token
    ]

    # Initialise the base Segment
    segment = Segment.from_dictionary(find_segment(base_string, segment_list))

    # Add each diacritic feature to the segment
    for diacritic in diacritics:
        diacritic_segment = Segment(
            diacritic["applies"].get("positive", []),
            diacritic["applies"].get("negative", []),
        )
        segment = segment + diacritic_segment

    return segment
