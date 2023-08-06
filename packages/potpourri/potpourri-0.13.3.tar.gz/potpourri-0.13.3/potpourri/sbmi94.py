
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeClassifier
import scipy.stats as ss

model = Pipeline(steps=[
    ('scl', StandardScaler()),
    ('lin', RidgeClassifier(
        solver = 'sag',
        tol = 0.001,  # optimizer termination criteria
        # alpha = 1.0,  # L2 regulization alpha=C^{-1}
        fit_intercept = True,
        class_weight = {0: 1, 1: 1},  # enforce binary [0,1]
        normalize = False,  # done in the pipeline
        copy_X = True,
        random_state = 42,   # for SAG/SAGA solver
    ))
])

hyper = {
    # 'lin__alpha': ss.expon(loc=1e-8, scale=.1),
    # 'lin__alpha': ss.uniform(1e-4, 1.1),   # C ~ [1/1.1, 10000]
    # 'lin__alpha': ss.gamma(a=2.2, loc=1e-5, scale=.7),  # alpha~[0.004, 9.8]
    'lin__alpha': ss.gamma(a=1.5, loc=1e-5, scale=.7),  # alpha~[0.001, 10]
}

meta = {
    'id': "sbmi94",
    'name': 'Logistic Ridge',
    'descriptions': (
        "Logistic Regression, L2 penalty (Ridge), SAG solver, standard-normal "
        "transformed features."),
    'solver': 'Stochastic Average Gradient descent (SAG)',
    'active': True,
    'keywords': [
        'binary classification', 'linear regression', 'RidgeClassifier'],
    'output_num': 'single',
    'output_scale': 'binary',
    'output_dtype': 'bool',
    'input_num': 'multi',
    'input_scale': 'interval',
    'input_dtype': 'float'
}
