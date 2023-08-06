
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LassoLars
import scipy.stats as ss

model = Pipeline(steps=[
    ('scl', StandardScaler()),
    ('lin', LassoLars(
        fit_intercept=True,
        positive = False,
        precompute = True,
        eps = 2.220446049250313e-16,  # for ill-conditioned cholesky
        max_iter = 500,
        normalize=True,
        copy_X = True,
        fit_path = False,  # set to True for debugging "model.coef_path_"
        verbose = False,  # for debugging
    ))
])

hyper = {
    'lin__alpha': ss.gamma(a=2.2, loc=1e-3, scale=0.7),
}

meta = {
    'id': "simi2",
    'name': 'LinReg Lasso',
    'descriptions': 'Lasso Regression (L1 penalty), LARS solver.',
    'solver': 'Least Angle Regression (LARS)',
    'active': True,
    'keywords': [
        'linear regression', 'univariate regression', 'multiple regression'],
    'output_num': 'single',
    'output_scale': 'interval',
    'output_dtype': 'float',
    'input_num': 'multi',
    'input_scale': 'interval',
    'input_dtype': 'float'
}
