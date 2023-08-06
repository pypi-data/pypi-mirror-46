from .dim4 import PcaModelSelect

trans = PcaModelSelect(score='aic', tol=1e-2)

meta = {
    'id': 'dim5',
    'name': 'PCA AIC',
    'description': (
        "Number of components is determined by fitting a Lasso-Logit "
        "model and minimize the AIC criteron."),
    'keywords': [
        'dimensionality reduction', 'principal component anlysis',
        'StandardScaler', 'PCA', 'AIC', 'Logistic Regression',
        'statsmodels'],
    'feature_names_prefix': 'dim_aic'
}

"""Example

from verto.dim5 import trans, meta
from datasets.demo1 import X_train, Y_train
from seasalt import create_feature_names
import pandas as pd
import numpy as np

#trans.set_params(**{'verbose': True, 'tol': 1e-2})
X_new = trans.fit_transform(X_train, Y_train)
names = create_feature_names(meta['feature_names_prefix'], X_new.shape[1])
df = pd.DataFrame(data=X_new, columns=names)
df
"""
