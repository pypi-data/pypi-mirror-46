from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import OneHotEncoder
from seasalt import ClusterTransformer
import numpy as np


class KMeansOnehot(Pipeline):
    def __init__(self, n_clusters=3):
        super().__init__(steps=[
            ('scl', StandardScaler()),  # with_mean=True,with_std=True
            ('kmeans', ClusterTransformer(MiniBatchKMeans(n_clusters = 3))),
            ('onehot', OneHotEncoder(sparse=False, categories='auto'))
        ])
        super().set_params(**{'kmeans__model__n_clusters': n_clusters})

    def set_params(self, **kwargs):
        if 'n_clusters' in kwargs:
            super().set_params(
                **{'kmeans__model__n_clusters': kwargs['n_clusters']})

    def transform(self, X, y=None):
        return super().transform(X).astype(np.int8)


trans = KMeansOnehot()

meta = {
    'id': 'clu1',
    'name': 'KMeans OneHot',
    'description': (
        "Onehot encoded KMeans clusters "),
    'keywords': [
        'KMeans', 'clustering', 'unsupervised',
        'StandardScaler', 'OneHotEncoder', 'MiniBatchKMeans'],
    'feature_names_prefix': 'clu_km'
}

"""Example

from verto.clu1 import trans, meta
from datasets.demo1 import X_train
from seasalt import create_feature_names
import pandas as pd
import numpy as np

trans.set_params(**{'n_clusters': 4})
X_new = trans.fit_transform(X_train)
names = create_feature_names(meta['feature_names_prefix'], X_new.shape[1])
df = pd.DataFrame(data=X_new, columns=names)
df
"""
