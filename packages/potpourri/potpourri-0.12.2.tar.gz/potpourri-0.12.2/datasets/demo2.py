# Breast Cancer Wisconsin
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import minmax_scale
import numpy as np

tmp = load_diabetes()

X_train, X_valid, Y_train, Y_valid = train_test_split(
    tmp.data,
    tmp.target,
    test_size = 0.30,
    random_state = 42
)
del tmp

# generate random folds
fold_ids = np.random.randint(low=1, high=10, size=(len(Y_train),))

# meta data
meta = {
    "id": "demo1",
    "name": "Diabetes datasets",
    "descriptions": (
        "Demo dataset from sklearn. Single ratio-scale output with integer "
        "values between 25 and 365. All inputs has been transformed to "
        "standard-normal interval-scaled features."),
    "source": (
        "https://scikit-learn.org/stable/modules/generated/"
        "sklearn.datasets.load_diabetes.html"),
    "keywords": [
        "demo dataset", "multivariate regression", "interval-scale features"],
    "sample_size": 442,
    "sample_train": len(Y_train),
    "sample_valid": len(Y_valid),
    'output_num': 1,  # 'single'
    'output_scale': 'ratio',
    'output_dtype': 'integer',
    'input_num': 10,  # 'multi'
    'input_scale': 'interval',
    'input_dtype': 'float'
}
