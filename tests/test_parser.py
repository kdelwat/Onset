import sys
import os.path as path

base_directory = path.dirname(path.dirname(path.abspath(__file__)))

sys.path.append(path.join(base_directory, 'app'))

from parse import tokenise, valid_subword

available_segments = ['ɒ', 'ɑ', 'ɶ', 'a', 'æ', 'ʌ', 'ɔ', 'o', 'ɤ', 'ɘ', 'œ', 'ə', 'e', 'ɞ', 'ø', 'ɛ', 'ɵ', 'ɯ', 'u', 'ʊ', 'ɨ', 'ʉ', 'y', 'i', 'ʏ', 'ɪ', 'ŋ̟', 'ʟ̟', 'ɫ', 'ɴ', 'ʀ', 'ɲ', 'ʎ', 'ŋ̟', 'ŋ̠', 'ʟ', 'ʟ̠', 'ɳ', 'ʙ', 'ɭ', 'ɺ', 'ɻ', 'ɽ', 'r', 'n', 'm', 'l', 'ɾ', 'ɱ', 'ʔ', 'ɣ̟', 'x̟', 'k̟', 'ɡ̟', 'k̟͡x̟', 'ɡ̟͡ɣ̟', 'ħ', 'ʕ', 'ʁ', 'q', 'χ', 'ɢ', 'ɕ', 'ɟ', 'ʝ', 'c', 'ç', 'd͡ʑ', 't͡ɕ', 'ɣ', 'ɣ̠', 'x', 'x̠', 'k', 'k̠', 'ɡ', 'ɡ̠', 'ʑ', 'ʈ', 'ɖ', 'ɬ', 'ʐ', 'ɸ', 'ʂ', 'ʒ', 'z', 'v', 't', 'ʃ', 's', 'p', 'f', 'd', 'b', 'θ', 'ɮ', 'ð', 'β', 'd͡ʒ', 'd͡z', 'd͡ɮ', 'd̠͡ɮ̠', 't͡ʃ', 't̠͡ɬ̠', 't͡s', 't͡ɬ', 't̪͡s̪', 't̪͡ɬ̪', 'd̪͡z̪', 'd̪͡ɮ̪', 'ʈ͡ʂ', 'ɖ͡ʐ', 'p͡f', 'b͡v', 'p͡ɸ', 'b͡β', 't̪͡θ', 'd̪͡ð', 'c͡ç', 'ɟ͡ʝ', 'k͡x', 'k̠͡x̠', 'ɡ͡ɣ', 'ɡ̠͡ɣ̠', 'q͡χ', 'ɢ͡ʁ', 'ɧ', 'k͡p', 'ɡ͡b', 'p͡t', 'b͡d', 'ɰ', 'ɰ̠', 'w', 'ɥ', 'j', 'ɹ', 'ʋ', 'ʍ', 'ɦ', 'h']

available_diacritics = ['ʰ', '\u0330']


def test_tokenise():
    assert tokenise('bok͡piʰ', available_segments, available_diacritics) == ['b', 'o', 'k͡p', 'iʰ']
    assert tokenise('', available_segments, available_diacritics) == []


def test_valid_subword():
    assert valid_subword('b', available_segments, available_diacritics)
    assert valid_subword('bʰ', available_segments, available_diacritics)
    assert valid_subword('bʰ\u0330', available_segments, available_diacritics)
    assert valid_subword('k̟͡x̟', available_segments, available_diacritics)

    assert not valid_subword('ʰ', available_segments, available_diacritics)
    assert not valid_subword('', available_segments, available_diacritics)
