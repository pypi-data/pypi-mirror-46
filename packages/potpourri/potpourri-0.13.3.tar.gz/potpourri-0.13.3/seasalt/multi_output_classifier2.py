from sklearn.base import BaseEstimator, ClassifierMixin
from copy import deepcopy
import numpy as np


class MultiOutputClassifier2(BaseEstimator, ClassifierMixin):
    def __init__(self, estimator):
        self.estimator = estimator

    def fit(self, X, y, **fit_params):
        # copy base estimators
        self.n_targets = y.shape[1]  # if len(y.shape) >= 2 else 1
        self.estimators_ = []
        for i in range(self.n_targets):
            self.estimators_.append(deepcopy(self.estimator))
        # adjust 'eval_set' in fit_params
        tmp_params = []
        for i in range(self.n_targets):
            tmp_params.append(deepcopy(fit_params))
            if 'eval_set' in tmp_params[i]:
                tmp_X = tmp_params[i]['eval_set'][0]
                tmp_y = tmp_params[i]['eval_set'][1]
                tmp_params[i]['eval_set'] = (tmp_X, tmp_y[:, i])
        # loop over each estimator
        for i in range(self.n_targets):
            self.estimators_[i].fit(X, y[:, i], **tmp_params[i])
        # retrive feature importances
        self.feature_importances_targets_ = np.vstack(
            [estim.feature_importances_ for estim in self.estimators_]).T
        self.feature_importances_ = np.sum(
            self.feature_importances_targets_, axis=1)
        return self

    def predict_proba(self, X):
        return [estim.predict_proba(X) for estim in self.estimators_]

    def predict(self, X):
        tmp = [estim.predict(X) for estim in self.estimators_]
        return np.stack(tmp, axis=1)

    def score(self, X, y):
        y_pred = self.predict(X)
        return np.mean(np.all(y == y_pred, axis=1))
