from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


trans = Pipeline(steps=[
    ('scl', StandardScaler(with_mean=True, with_std=True, copy=True)),
    ('pca', PCA(
        n_components='mle', svd_solver='full',
        whiten=False, copy=True))
])

meta = {
    'id': 'dim2',
    'name': 'PCA Minka MLE',
    'description': "Minka's MLE to guess n_components",
    'keywords': [
        'dimensionality reduction', 'principal component anlysis',
        'StandardScaler', 'PCA', 'Minka MLE'],
    'feature_names_prefix': 'dim_minka'
}


"""Example

from verto.dim2 import trans, meta
from datasets.demo1 import X_train
from seasalt import create_feature_names
import pandas as pd
import numpy as np

X_new = trans.fit_transform(X_train).astype(np.float16)
names = create_feature_names(meta['feature_names_prefix'], X_new.shape[1])
df = pd.DataFrame(data=X_new, columns=names)
df
"""
