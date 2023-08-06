
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNet
import scipy.stats as ss

model = Pipeline(steps=[
    ('scl', StandardScaler()),
    ('lin', ElasticNet(
        fit_intercept = True,
        positive = False,
        random_state = 42,
        selection = 'random',
        precompute = True,
        tol = 0.0001,
        max_iter = 1000,
        warm_start = True,
        normalize = False,  # done in the pipeline
        copy_X = True,
    ))
])

hyper = {
    'lin__alpha': ss.gamma(a=2.2, loc=1e-3, scale=0.7),
    'lin__l1_ratio': ss.uniform(0, 1),
}

meta = {
    'id': "simi4",
    'name': 'LinReg ElasticNet',
    'descriptions': (
        "ElasticNet Regression (L1/L2 penalty), Coordinate Descent solver."),
    'solver': 'Coordinate Descent',
    'active': True,
    'keywords': [
        'linear regression', 'univariate regression', 'multiple regression',
        'elasticnet', 'sklearn.linear_model.ElasticNet'],
    'output_num': 'single',
    'output_scale': 'interval',
    'output_dtype': 'float',
    'input_num': 'multi',
    'input_scale': 'interval',
    'input_dtype': 'float'
}
