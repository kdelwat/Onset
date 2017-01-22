import sys
import os.path as path

base_directory = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(path.join(base_directory, 'app'))

from word import Word


def test_overlapping_chunks():
    word = Word([])
    assert word.overlapping_chunks([], 3) == []
    assert word.overlapping_chunks([1, 2, 3, 4, 5], 2) == [[1, 2],
                                                           [2, 3],
                                                           [3, 4],
                                                           [4, 5]]
    assert word.overlapping_chunks([1, 2, 3, 4, 5], 3) == [[1, 2, 3],
                                                           [2, 3, 4],
                                                           [3, 4, 5]]
