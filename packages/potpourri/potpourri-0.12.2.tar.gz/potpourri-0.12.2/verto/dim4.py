from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
import statsmodels.api as sm


class PcaModelSelect(Pipeline):
    """Principal component analysis (PCA) wheras the number
    of components by simple backtracking line search and
    model selection criteria

    Parameters
    ----------
    score : str (Default: 'bic')
        The model selection criteria to minimze
        - 'bic' (default)
        - 'aic'
        - 'prsquared'

    tol : float (Default: 1e-3)
        Required percentage decrease in each iteration.

    max_iter: int (Default: None)
        Any number between 1 and the number of features

    verbose: bool (Default: False)

    Algorithm
    ---------
        1. Increment the number of components by one
        2. Run the PCA
        3. Fit a Lasso-Logit model with the components
        4. Check if model selection criteria improves
        5. If not, terminate backtracking; Else got to 1
    """
    def __init__(self, score='bic', tol=1e-3, verbose=False, max_iter=None,
                 alpha=1.0):
        self.score = score
        self.tol = tol
        self.verbose = verbose
        self.max_iter = max_iter
        self.alpha = alpha
        super().__init__(steps=[
            ('scl', StandardScaler(with_mean=True, with_std=True, copy=True)),
            ('pca', PCA(
                n_components=1,
                svd_solver='full', whiten=False, copy=True))
        ])

    def transform(self, X, y=None):
        return super().transform(X).astype(np.float16)

    def fit(self, X, y):
        # start values
        prev = None
        redu = 1.0
        status = 'proceed'

        # max n_components
        if self.max_iter is None:
            self.max_iter = X.shape[1]
        max_iter = min(self.max_iter, X.shape[1])

        # display
        if self.verbose:
            print("{:3s} | {:8s} | {:8s} | {}".format(
                'num', 'score', 'improved', 'status'))

        # backtracking loop
        for n_comp in range(1, max_iter):
            # set PCA parameter
            super().set_params(**{'pca__n_components': n_comp})

            # compute components
            X_new = super().fit_transform(X)

            # run Logistic Regression
            lr = sm.Logit(y, sm.add_constant(X_new)).fit_regularized(
                method='l1', alpha=self.alpha, disp=0)

            # read current score (target fun value to minimize)
            curr = getattr(lr, self.score)
            if self.score == 'prsquared':
                curr = 1 - curr

            # minimization task
            if prev is None:
                prev = curr  # First iteration
            else:
                redu = 1 - curr / prev
                prev = curr
                if redu > self.tol:
                    self.best_n_components_ = n_comp
                    self.best_statsmodel_ = lr
                else:
                    status = 'terminated'
                    break

            # display - progress
            if self.verbose:
                print("{:3d} | {:8.4f} | {:8.4f} | {}".format(
                    n_comp, curr, redu, status))

        # display - final resul
        if self.verbose:
            print(self.best_statsmodel_.summary())

        # reset best solution
        super().set_params(**{'pca__n_components': self.best_n_components_})

    def fit_transform(self, X, y):
        self.fit(X, y)
        return self.transform(X)


trans = PcaModelSelect(score='bic', tol=1e-3)

meta = {
    'id': 'dim4',
    'name': 'PCA BIC',
    'description': (
        "Number of components is determined by fitting a Lasso-Logit "
        "model and minimize the BIC criteron."),
    'keywords': [
        'dimensionality reduction', 'principal component anlysis',
        'StandardScaler', 'PCA', 'BIC', 'Logistic Regression',
        'statsmodels'],
    'feature_names_prefix': 'dim_bic'
}

"""Example

from verto.dim4 import trans, meta
from datasets.demo1 import X_train, Y_train
from seasalt import create_feature_names
import pandas as pd
import numpy as np

#trans.set_params(**{'verbose': True, 'tol': 1e-3})
X_new = trans.fit_transform(X_train, Y_train)
names = create_feature_names(meta['feature_names_prefix'], X_new.shape[1])
df = pd.DataFrame(data=X_new, columns=names)
df
"""
