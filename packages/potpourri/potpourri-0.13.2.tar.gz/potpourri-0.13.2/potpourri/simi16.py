
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import TheilSenRegressor
import scipy.stats as ss

model = Pipeline(steps=[
    ('scl', StandardScaler()),
    ('lin', TheilSenRegressor(
        fit_intercept = True,
        copy_X = True,
        max_subpopulation = 10000,  # constrain 'n choose k' to 10k
        n_subsamples = None,  # maximal robustness
        max_iter = 300,
        tol = 1e-3,
        random_state = 42
    ))
])

hyper = {
    # 'lin__epsilon': ss.uniform(1.0, 6.0),  # threshold for standardized error
    # 'lin__alpha': ss.gamma(a=1.5, loc=1e-5, scale=.7),  # alpha ~ [0.001, 10]
}

meta = {
    'id': "simi16",
    'name': 'LinReg Theil-Sen',
    'descriptions': (
        "Theil-Sen Regression, standard-normal transformed features."),
    'solver': 'L-BFGS',
    'active': True,
    'keywords': [
        'robust regression', 'univariate regression', 'multiple regression',
        'theil-sen regression', 'sklearn.linear_model.TheilSenRegressor',
        'theil-sen estimator', 'sen slope estimator', 'slope selection',
        'single-median method', 'kendall robust line-fit method',
        'kendall–theil robust line'],
    'output_num': 'single',
    'output_scale': 'interval',
    'output_dtype': 'float',
    'input_num': 'multi',
    'input_scale': 'interval',
    'input_dtype': 'float'
}
