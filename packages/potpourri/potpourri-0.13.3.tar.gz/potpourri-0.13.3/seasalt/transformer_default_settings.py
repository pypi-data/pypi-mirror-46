from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import itertools as it
from seasalt import create_feature_names


class TransformerDefaultSettings(BaseEstimator, TransformerMixin):
    def __init__(self, module_list):
        self.module_list = module_list
        # import modules
        self.modules_ = []
        for m in self.module_list:
            self.modules_.append(__import__(m, fromlist=['trans', 'meta']))

    def fit(self, X, y=None):
        # fit modules
        for i in range(len(self.modules_)):
            self.modules_[i].trans.fit(X, y)
        return self

    def transform(self, X, y=None):
        Z = []
        for i in range(len(self.modules_)):
            Z.append(self.modules_[i].trans.transform(X))

        # create names if not exist
        if not hasattr(self, 'feature_names_'):
            f = []
            for i in range(len(self.modules_)):
                f.append(create_feature_names(
                    self.modules_[i].meta['feature_names_prefix'],
                    Z[i].shape[1]))
            self.feature_names_ = list(it.chain.from_iterable(f))

        return np.concatenate(Z, axis=1)


"""
Example

trn = TransformerDefaultSettings(["verto.raw1", "verto.rnd1"])
trn.fit(X_train, Y_train)
X_new = trn.transform(X_train)
pd.DataFrame(data=X_new, columns=trn.feature_names_)
"""
