# Breast Cancer Wisconsin
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import minmax_scale
import numpy as np

tmp = load_breast_cancer()

X_train, X_valid, Y_train, Y_valid = train_test_split(
    minmax_scale(tmp.data, axis=0),
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
    "name": "Breast Cancer Wisconsin",
    "descriptions": (
        "Demo dataset from sklearn. Binary output labels indicate cancer "
        "or not. Original input features are min-max transformed to "
        "ratio-scaled features."),
    "source": (
        "https://scikit-learn.org/stable/modules/generated/"
        "sklearn.datasets.load_breast_cancer.html"),
    "keywords": [
        "demo dataset", "binary classification", "interval-scale features"],
    "sample_size": 569,
    "sample_train": len(Y_train),
    "sample_valid": len(Y_valid),
    'output_num': 1,  # 'single'
    'output_scale': 'binary',
    'output_dtype': 'bool',
    'input_num': 30,  # 'multi'
    'input_scale': 'ratio',
    'input_dtype': 'float'
}
