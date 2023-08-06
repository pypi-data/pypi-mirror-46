# Refit
from copy import deepcopy


def refit_model(basemodel, newparams, X, y=None):
    newmodel = deepcopy(basemodel)
    newmodel.set_params(**newparams)
    newmodel.fit(X, y)
    return newmodel
