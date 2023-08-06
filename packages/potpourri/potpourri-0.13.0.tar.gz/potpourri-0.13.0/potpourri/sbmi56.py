
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import scipy.stats as ss

model = Pipeline(steps=[
    ('scl', StandardScaler()),
    ('lin', LogisticRegression(
        penalty = 'l1',
        solver = 'liblinear',  # for L1
        multi_class = 'ovr',  # binary
        random_state = 42,
        fit_intercept = True,
        max_iter = 100,
    ))
])

hyper = {
    'lin__C': ss.gamma(a=2.2, loc=1e-3, scale=0.7),
    'lin__intercept_scaling': ss.uniform(.1, 1.9),
    # 'lin__fit_intercept': [True, False]
}

meta = {
    'id': "sbmi56",
    'name': 'Logistic Lasso',
    'descriptions': 'Logistic Regression with L1 penalty (Lasso)',
    'solver': 'liblinear',
    'active': True,
    'keywords': ['binary classification', 'linear regression'],
    'output_num': 'single',
    'output_scale': 'binary',
    'output_dtype': 'bool',
    'input_num': 'multi',
    'input_scale': 'interval',
    'input_dtype': 'float'
}
