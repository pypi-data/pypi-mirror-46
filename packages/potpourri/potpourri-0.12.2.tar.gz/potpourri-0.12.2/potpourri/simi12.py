
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LassoLarsIC


model = Pipeline(steps=[
    ('scl', StandardScaler()),
    ('lin', LassoLarsIC(
        fit_intercept=True,
        positive = False,
        precompute = True,
        eps = 2.220446049250313e-16,  # for ill-conditioned cholesky
        max_iter = 500,
        normalize=True,
        copy_X = True,
        verbose = False,  # for debugging
    ))
])

hyper = {
    'lin__criterion': ['aic', 'bic'],
}

meta = {
    'id': "simi12",
    'name': 'LinReg Lasso IC',
    'descriptions': (
        "Lasso Regression (L1 penalty), LARS solver, Autoselect l1 penalty "
        "based on information criteria aic or bic"),
    'solver': 'Least Angle Regression (LARS)',
    'active': True,
    'keywords': [
        'linear regression', 'univariate regression', 'multiple regression',
        'model selection', 'LassoLarsIC'],
    'output_num': 'single',
    'output_scale': 'interval',
    'output_dtype': 'float',
    'input_num': 'multi',
    'input_scale': 'interval',
    'input_dtype': 'float'
}
