from sklearn.ensemble import IsolationForest
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np


class IsolationForestTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, model):
        self.model = model

    def fit(self, *args, **kwargs):
        self.model.fit(*args, **kwargs)
        return self

    def transform(self, X, **transform_params):
        return self.model.score_samples(X).astype(np.float16).reshape(-1, 1)


trans_base = IsolationForest(
    n_estimators = 96,  # number of base trees
    contamination = 0.1,  # pct of outliers = pct of TRUE targets
    max_samples = 'auto',  # to train 1 base tree; 'auto'=max(256, n_samples)
    max_features = 1.0,   # use all features
    # other
    bootstrap = False,  # False: without replacement; Don't reuse
    random_state = 42,
    behaviour = 'new',
    verbose = False,
    n_jobs = -1
)

trans = IsolationForestTransformer(trans_base)

meta = {
    'id': 'out1',
    'name': 'Iso. Forest',
    'description': (
        "Isolation Forest partitions samples randomly. The path length "
        "(or number of splits) is short for anomalies (anomal samples)"),
    'keywords': [
        'IsolationForest', 'Isolation Forest', "outlier detection"],
    'feature_names_prefix': 'out_iso'
}

"""Example

from verto.out1 import trans, meta
from datasets.demo1 import X_train, Y_train
from seasalt import create_feature_names
import pandas as pd
import numpy as np

trans.set_params(**{'model__contamination': 0.2})
X_new = trans.fit_transform(X_train)
names = create_feature_names(meta['feature_names_prefix'], X_new.shape[1])
df = pd.DataFrame(data=X_new, columns=names)
df
"""
