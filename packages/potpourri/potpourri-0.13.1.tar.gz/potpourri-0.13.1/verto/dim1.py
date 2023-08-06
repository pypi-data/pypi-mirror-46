from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


trans = Pipeline(steps=[
    ('scl', StandardScaler(with_mean=True, with_std=True, copy=True)),
    ('pca', PCA(n_components = 1, svd_solver='auto', whiten=False, copy=True))
])

meta = {
    'id': 'dim1',
    'name': 'PCA',
    'description': "PCA with given number of components",
    'keywords': [
        'dimensionality reduction', 'principal component anlysis',
        'StandardScaler', 'PCA'],
    'feature_names_prefix': 'dim_pca'
}


"""Example

from verto.dim1 import trans, meta
from datasets.demo1 import X_train
from seasalt import create_feature_names
import pandas as pd
import numpy as np

trans.set_params(**{'pca__n_components': 3})
X_new = trans.fit_transform(X_train).astype(np.float16)
names = create_feature_names(meta['feature_names_prefix'], X_new.shape[1])
df = pd.DataFrame(data=X_new, columns=names)
df
"""
