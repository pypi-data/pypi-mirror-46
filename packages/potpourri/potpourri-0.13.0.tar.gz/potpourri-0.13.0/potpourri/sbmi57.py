
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDClassifier
import scipy.stats as ss

model = Pipeline(steps=[
    ('scl', StandardScaler()),
    ('lin', SGDClassifier(
        # Logistic Regression
        loss = 'log',
        penalty = 'l1',
        l1_ratio = 1,
        fit_intercept = True,
        # solver settings
        max_iter = 1000,
        tol = 1e-3,
        shuffle = True,
        random_state = 42,
        # adaptive learning
        learning_rate = 'adaptive',
        eta0 = 0.5,
        # early stopping
        early_stopping = True,
        validation_fraction = 0.15,
        n_iter_no_change = 10,
        # other
        warm_start = True,
        average = False,  # disable for Lasso!
    ))
])

hyper = {
    'lin__alpha': ss.expon(loc=1e-8, scale=.1),
    # 'lin__fit_intercept': [True, False]
}

meta = {
    'id': "sbmi57",
    'name': 'Logistic Lasso',
    'descriptions': 'Logistic Regression with L1 penalty (Lasso)',
    'solver': 'stochastic gradient descent',
    'active': True,
    'keywords': ['binary classification', 'linear regression'],
    'output_num': 'single',
    'output_scale': 'binary',
    'output_dtype': 'bool',
    'input_num': 'multi',
    'input_scale': 'interval',
    'input_dtype': 'float'
}
