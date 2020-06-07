import sys
import os.path as path
import numpy as np

from engine.feature_vector import fv_sum

base_directory = path.dirname(path.dirname(path.abspath(__file__)))

sys.path.append(path.join(base_directory, "engine"))


def test_fv_sum_identity():
    fvs = [
        np.array([1, -1, 0, 1, -1, 0]),
        np.array([1, -1, 0, 1, -1, 0]),
        np.array([1, -1, 0, 1, -1, 0]),
    ]

    assert np.array_equal(fv_sum(fvs), np.array([1, -1, 0, 1, -1, 0]))


def test_fv_sum():
    fvs = [
        np.array([1, -1, 0, 1, -1, 0]),
        np.array([1, 1, 1, 1, -1, 0]),
        np.array([0, 0, 0, -1, 1, 1]),
    ]

    assert np.array_equal(fv_sum(fvs), np.array([1, 1, 1, -1, 1, 1]))
