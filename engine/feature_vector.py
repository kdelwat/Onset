from typing import List, NewType
import numpy as np

FeatureVector = NewType("FeatureVector", np.ndarray)

# To sum feature vectors, we want the latest non-zero value of a column
uf_sum = np.frompyfunc(lambda a, b: a if b == 0 else b, 2, 1)


def fv_sum(fvs: List[FeatureVector]) -> FeatureVector:
    return uf_sum.reduce(fvs).astype(np.int8)


def fv_show(fv: FeatureVector) -> str:
    repr = ""

    for f in fv:
        if f == -1:
            repr += "-"
        elif f == 1:
            repr += "+"
        else:
            repr += "0"

    return repr
