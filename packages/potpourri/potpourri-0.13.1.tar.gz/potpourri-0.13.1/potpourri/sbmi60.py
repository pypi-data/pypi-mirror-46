
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDClassifier
import scipy.stats as ss

model = Pipeline(steps=[
    ('scl', StandardScaler()),
    ('lin', SGDClassifier(
        # Logistic Regression
        loss = 'log',
        penalty = 'l2',
        l1_ratio = 0,
        fit_intercept = True,
        class_weight = {0: 1, 1: 1},  # enforce binary [0,1]
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
        average = 20,  # after 20 epochs, compute average weights
    ))
])

hyper = {
    # 'lin__alpha': ss.expon(loc=1e-8, scale=.1),
    # 'lin__alpha': ss.uniform(1e-4, 1.1),   # C ~ [1/1.1, 10000]
    # 'lin__alpha': ss.gamma(a=2.2, loc=1e-5, scale=.7),  # alpha~[0.004, 9.8]
    'lin__alpha': ss.gamma(a=1.5, loc=1e-5, scale=.7),  # alpha ~ [0.001, 10]
}

meta = {
    'id': "sbmi60",
    'name': 'Logistic Ridge',
    'descriptions': (
        "Logistic Regression, L2 penalty (Ridge), SGD solver, standard-normal "
        "transformed features."),
    'solver': 'Stochastic Gradient Descent (SGD)',
    'active': True,
    'keywords': [
        'binary classification', 'linear regression', 'SGDClassifier'],
    'output_num': 'single',
    'output_scale': 'binary',
    'output_dtype': 'bool',
    'input_num': 'multi',
    'input_scale': 'interval',
    'input_dtype': 'float'
}
