
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
import scipy.stats as ss

model = Pipeline(steps=[
    ('scl', StandardScaler()),
    ('lin', LogisticRegression(
        penalty = 'l1',
        solver = 'saga',   # for L1
        multi_class = 'ovr',  # binary
        random_state = 42,
        fit_intercept = True,
        max_iter = 100,
        warm_start = True,  # reuse previous solution
    ))
])

hyper = {
    'lin__C': ss.gamma(a=2.2, loc=1e-3, scale=0.7),
    # 'lin__fit_intercept': [True, False]
}

meta = {
    'id': "sbmi1",
    'name': 'Logistic Lasso',
    'descriptions': 'Logistic Regression with L1 penalty (Lasso)',
    'solver': 'SAGA',
    'active': True,
    'keywords': ['binary classification', 'linear regression'],
    'output_num': 'single',
    'output_scale': 'binary',
    'output_dtype': 'bool',
    'input_num': 'multi',
    'input_scale': 'interval',
    'input_dtype': 'float'
}
