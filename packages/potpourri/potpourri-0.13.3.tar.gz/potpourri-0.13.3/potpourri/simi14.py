
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ARDRegression
import scipy.stats as ss

model = Pipeline(steps=[
    ('scl', StandardScaler()),
    ('lin', ARDRegression(
        tol = 0.001,
        n_iter = 300,
        fit_intercept = True,
        normalize = False,
        compute_score = False,
        copy_X = True,
        verbose = False,
    ))
])

hyper = {
    'lin__alpha_1': ss.expon(loc=1e-7, scale=.01),
    'lin__alpha_2': ss.expon(loc=1e-7, scale=.01),
    'lin__lambda_1': ss.expon(loc=1e-7, scale=.01),
    'lin__lambda_2': ss.expon(loc=1e-7, scale=.01),
    # 'lin__threshold_lambda': ss.randint(5, 10000),
}

meta = {
    'id': "simi14",
    'name': 'LinReg ARD',
    'descriptions': 'Automatic Relevance Determination',
    'solver': 'Evidence Maximization',
    'active': True,
    'keywords': [
        'linear regression', 'univariate regression', 'multiple regression',
        'bayesian regression', 'maximum likelihood estimation',
        'automatic relevance determination',
        'sparse bayesian learning and relevance vector machine',
        'sklearn.linear_model.ARDRegression'],
    'output_num': 'single',
    'output_scale': 'interval',
    'output_dtype': 'float',
    'input_num': 'multi',
    'input_scale': 'interval',
    'input_dtype': 'float'
}
