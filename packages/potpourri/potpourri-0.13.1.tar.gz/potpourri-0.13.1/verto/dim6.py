from .dim4 import PcaModelSelect

trans = PcaModelSelect(score='prsquared', tol=0.05)

meta = {
    'id': 'dim6',
    'name': 'PCA Pseudo R^2',
    'description': (
        "Number of components is determined by fitting a Lasso-Logit "
        "model and maximize the Pseudo R^2 (McFadden) score."),
    'keywords': [
        'dimensionality reduction', 'principal component anlysis',
        'StandardScaler', 'PCA', 'Pseudo R^2', 'Logistic Regression',
        'statsmodels'],
    'feature_names_prefix': 'dim_prsq'
}

"""Example

from verto.dim6 import trans, meta
from datasets.demo1 import X_train, Y_train
from seasalt import create_feature_names
import pandas as pd
import numpy as np

#trans.set_params(**{'verbose': True, 'tol': 0.05})
X_new = trans.fit_transform(X_train, Y_train)
names = create_feature_names(meta['feature_names_prefix'], X_new.shape[1])
df = pd.DataFrame(data=X_new, columns=names)
df
"""
