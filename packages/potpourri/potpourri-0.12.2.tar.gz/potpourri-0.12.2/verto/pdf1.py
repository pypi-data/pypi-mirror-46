from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


def getidx(i, n_bins):
    return min(i - 1, n_bins - 1)


def lookup(h, b, X, n_bins):
    return [h[getidx(np.searchsorted(b, xi), n_bins)] for xi in X]


class HistDensity(BaseEstimator, TransformerMixin):
    def __init__(self, bins=512):
        self.n_bins = bins

    def fit(self, X, y=None):
        # declare variables
        n_features = X.shape[1]
        self.hist_density_ = np.empty(shape=(self.n_bins, n_features))
        self.bin_edges_ = np.empty(shape=(self.n_bins + 1, n_features))
        # compute histogram for each feature
        for j in range(n_features):
            self.hist_density_[:, j], self.bin_edges_[:, j] = np.histogram(
                X[~np.isnan(X[:, j]), j], bins=self.n_bins, density=True)
        return self

    def transform(self, X, y=None):
        # declare variables
        n_features = self.hist_density_.shape[1]
        output = np.empty(shape=X.shape)
        # lookup densities from fitted histograms
        # getidx=lambda i: min(i - 1, self.n_bins - 1)
        # lookup=lambda h, b, X: [h[getidx(np.searchsorted(b,xi))] for xi in X]
        for j in range(n_features):
            output[:, j] = lookup(
                self.hist_density_[:, j],
                self.bin_edges_[:, j],
                X[:, j],
                self.n_bins)
        return output


trans = HistDensity()

meta = {
    'id': 'pdf1',
    'name': 'Prob Density',
    'description': (
        "Probability density estimated by a histogram. "
        "Lookup density based on fitted bin edges"),
    'keywords': [
        'histogram', 'probability density'],
    'feature_names_prefix': 'pdf_hist'
}

"""Example

from verto.pdf1 import trans, meta
from datasets.demo1 import X_train, Y_train
from seasalt import create_feature_names
import pandas as pd
import numpy as np

trans.set_params(**{'bins': 128})
X_new = trans.fit_transform(X_train)
names = create_feature_names(meta['feature_names_prefix'], X_new.shape[1])
df = pd.DataFrame(data=X_new, columns=names)
df
"""
