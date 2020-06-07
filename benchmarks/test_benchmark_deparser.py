from engine.data import load_feature_strings, load_diacritics, load_segments
from engine.deparse import deparse_words
from engine.parse import parse_words

# Currently sitting at 21.14 seconds (median)
def test_deparse_words(benchmark):
    word_strings = ["bæd", "bɔɪ", "b\u02D0ɒtl"] * 100

    segments = load_segments()
    diacritics = load_diacritics()
    feature_strings = load_feature_strings()

    words = parse_words(word_strings, segments, diacritics)

    deparsed_words = benchmark(deparse_words, words, feature_strings)

    assert deparsed_words == word_strings
