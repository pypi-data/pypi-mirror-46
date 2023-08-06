
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import HuberRegressor
import scipy.stats as ss

model = Pipeline(steps=[
    ('scl', StandardScaler()),
    ('lin', HuberRegressor(
        fit_intercept = True,
        max_iter = 100,
        warm_start = True,
        tol = 1e-5
    ))
])

hyper = {
    'lin__epsilon': ss.uniform(1.0, 6.0),  # threshold for standardized error
    'lin__alpha': ss.gamma(a=1.5, loc=1e-5, scale=.7),  # alpha ~ [0.001, 10]
}

meta = {
    'id': "simi15",
    'name': 'LinReg Huber',
    'descriptions': (
        "Huber Regression, L-BFGS solver, standard-normal transformed "
        "features."),
    'solver': 'L-BFGS',
    'active': True,
    'keywords': [
        'robust regression', 'univariate regression', 'multiple regression',
        'huber regression', 'outlier', 'sklearn.linear_model.HuberRegressor',
        'huber', 'z-score'],
    'output_num': 'single',
    'output_scale': 'interval',
    'output_dtype': 'float',
    'input_num': 'multi',
    'input_scale': 'interval',
    'input_dtype': 'float'
}
