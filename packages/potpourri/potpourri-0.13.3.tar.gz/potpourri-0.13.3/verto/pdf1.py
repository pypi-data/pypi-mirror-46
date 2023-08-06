from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


def lookup(h, b, X, n_bins):
    idx_raw = np.searchsorted(b, X)
    idx_adj = np.minimum(idx_raw - 1, n_bins - 1)
    return h[idx_adj]


class HistDensity(BaseEstimator, TransformerMixin):
    def __init__(self, bins=512):
        self.n_bins = bins

    def fit(self, X, y=None):
        # circumvent BUG in sklearn's cross_validate, RandomizedSearchCV
        bins_tmp = self.n_bins if self.n_bins else 512
        # declare variables
        n_features = X.shape[1]
        self.hist_density_ = np.empty(shape=(bins_tmp, n_features))
        self.bin_edges_ = np.empty(shape=(bins_tmp + 1, n_features))
        # compute histogram for each feature
        for j in range(n_features):
            self.hist_density_[:, j], self.bin_edges_[:, j] = np.histogram(
                X[~np.isnan(X[:, j]), j], bins=bins_tmp, density=True)
        return self

    def transform(self, X, y=None):
        # circumvent BUG in sklearn's cross_validate, RandomizedSearchCV
        bins_tmp = self.n_bins if self.n_bins else 512
        # declare variables
        n_features = self.hist_density_.shape[1]
        output = np.empty(shape=X.shape)
        # lookup densities from fitted histograms
        for j in range(n_features):
            output[:, j] = lookup(
                self.hist_density_[:, j],  # h
                self.bin_edges_[:, j],  # b
                X[:, j],  # X
                bins_tmp)
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
