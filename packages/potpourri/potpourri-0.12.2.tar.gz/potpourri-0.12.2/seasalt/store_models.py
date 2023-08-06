# Store the best model somewhere
# https://scikit-learn.org/stable/modules/model_persistence.html
import os
import pickle
import joblib
import warnings


def to_disk(model, fname, path="tmp", tech="joblib"):
    # convert relative path to absolute path
    if not os.path.isabs(path):
        path = os.getcwd() + '/' + path
    # create folders
    os.makedirs(path, exist_ok=True)
    # add trailing slash
    path = os.path.join(path, '')
    # store it
    if tech is "joblib":
        joblib.dump(model, path + fname + '.joblib')
    elif tech is "pickle":
        pickle.dump(model, open(path + fname + '.pickle', 'wb'))
    else:
        raise Exception("unknown tech='...' specified.")
    return None


def from_disk(fname, path="tmp", tech="joblib"):
    # add trailing slash
    path = os.path.join(path, '')
    # load and return the model
    if tech is "joblib":
        filename = path + fname + '.joblib'
        if os.path.isfile(filename):  # check if file exist
            return joblib.load(filename)
    elif tech is "pickle":
        filename = path + fname + '.pickle'
        if os.path.isfile(filename):  # check if file exist
            return pickle.loads(open(filename, 'rb'))
    else:
        raise Exception("unknown tech='...' specified.")
    # file does not exist
    warnings.warn("'{:s}' does not not exist.".format(filename))
    return None
