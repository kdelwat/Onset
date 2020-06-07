from engine.data import Segments, Diacritics
from engine.feature_vector import fv_sum
import numpy as np
import re
from typing import List, Pattern, AnyStr


# Construct a regex to match an IPA segment.
#
# The regex will match a phoneme, zero or more diacritics, and then optionally a phoneme and diacritics joined with the
# Unicode overhead combining mark (which captures digraphs).
#
# Precompiling the regex once allows us to match in O(n) time.
def create_segment_regex(segments: Segments, diacritics: Diacritics) -> Pattern[AnyStr]:
    all_segments = "".join(
        [segment for segment in segments.keys() if len(segment) == 1]
    )
    all_diacritics = "".join(diacritics.keys())

    return re.compile(
        f"[{all_segments}][{all_diacritics}]*(?:\u0361[{all_segments}][{all_diacritics}])?"
    )


def parse_words(
    strings: List[str], segments: Segments, diacritics: Diacritics
) -> List[np.ndarray]:
    """Given a list of word strings (in IPA), return a list of Word objects
    containing parsed segments. Use the given segment and diacritic dictionaries.

    """

    r = create_segment_regex(segments, diacritics,)

    words = []

    for word in strings:
        tokens = r.findall(word)

        parsed_word = np.array(
            [token_to_segment(token, segments, diacritics) for token in tokens],
            dtype=np.int8,
        )

        words.append(parsed_word)

    return words


def token_to_segment(
    token: str, segments: Segments, diacritics: Diacritics
) -> np.ndarray:
    """Converts a string token in IPA to Segment object, given
    a list of dictionaries representing segments and the same representing
    diacritics."""

    base_ipa_characters = []
    diacritic_characters = []

    for c in token:
        if c in segments.keys():
            base_ipa_characters.append(c)
        elif c in diacritics.keys():
            diacritic_characters.append(c)
        else:
            print(f"Warning: unrecognised character in token: {c}")

    # Isolate the base IPA segment string
    base_ipa = "".join(base_ipa_characters)

    feature_vectors = [segments.get(base_ipa, None)]
    feature_vectors.extend(
        [diacritics.get(diacritic, None) for diacritic in diacritic_characters]
    )
    feature_vectors = [v for v in feature_vectors if v is not None]

    return fv_sum(feature_vectors)
