
from sklearn.base import BaseEstimator, TransformerMixin


class ClusterTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, model):
        self.model = model

    def fit(self, *args, **kwargs):
        self.model.fit(*args, **kwargs)
        return self

    def transform(self, X, **transform_params):
        return self.model.predict(X).reshape(-1, 1)
