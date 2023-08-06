from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


class RandomFeature(BaseEstimator, TransformerMixin):
    def __init__(self, n_cols=1):
        self.n_cols = n_cols

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        n_rows = len(X)
        return np.random.standard_normal((n_rows, self.n_cols))


trans = RandomFeature()

meta = {
    'id': 'rnd1',
    'name': 'Random Feature',
    'description': (
        "Generate 1 or more random standard normal variable(s). "
        "Use it in pre-analysing feature importances."),
    'keywords': ['standard_normal'],
    'feature_names_prefix': 'rnd_std'
}
