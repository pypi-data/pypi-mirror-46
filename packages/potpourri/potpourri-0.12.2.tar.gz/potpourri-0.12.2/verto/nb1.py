from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.naive_bayes import GaussianNB
import numpy as np
from copy import deepcopy


class SimpleGNB(BaseEstimator, TransformerMixin):
    def __init__(self, proba=True, priors=None, var_smoothing=1e-09):
        self.proba = proba
        self.priors = priors
        self.var_smoothing = var_smoothing

    def fit(self, X, y):
        self.n_features = X.shape[1]  # if len(X.shape) >= 2 else 1
        self.n_targets = y.shape[1]  # if len(y.shape) >= 2 else 1
        self.models = []
        for i in range(self.n_targets):
            for j in range(self.n_features):
                tmp = GaussianNB(
                    priors=self.priors, var_smoothing=self.var_smoothing)
                tmp.fit(X=X[:, j].reshape(-1, 1), y=y[:, i].reshape(-1, 1))
                self.models.append(deepcopy(tmp))
        return self

    def transform(self, X, y=None):
        output = np.empty(
            dtype=np.float16, shape=(len(X), self.n_targets * self.n_features))
        for i in range(self.n_targets):
            for j in range(self.n_features):
                idx = i * self.n_features + j
                if self.proba:
                    output[:, idx] = self.models[idx].predict_proba(X)[:, 1]
                else:
                    output[:, idx] = self.models[idx].predict(X)
        return output


trans = SimpleGNB()

meta = {
    'id': 'nb1',
    'name': 'Simple GNBs',
    'description': (
        "Fit each combination of target and feature as a "
        "simple Naive Bayes model, and use the predictions "
        "as features."),
    'keywords': ['GaussianNB', 'naive bayes'],
    'feature_names_prefix': 'nb'
}
