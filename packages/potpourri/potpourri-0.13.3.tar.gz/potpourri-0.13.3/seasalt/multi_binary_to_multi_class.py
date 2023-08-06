from sklearn.base import BaseEstimator, TransformerMixin
from itertools import product
import numpy as np


class MultiBinaryToMultiClass(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, Y):
        _, self.n_cols = Y.shape
        self.mapping = list(product([0, 1], repeat=self.n_cols))
        return self

    def transform(self, Y):
        n_rows, _ = Y.shape
        out = np.empty(shape=(n_rows,))
        out[:] = np.nan
        for enc in range(len(self.mapping)):
            idx = np.all(Y == self.mapping[enc], axis=1)
            out[idx] = enc
        return out.astype(int)

    def inverse_transform(self, y):
        out = []
        for enc in y:
            out.append(self.mapping[int(enc)])
        return np.vstack(out)
