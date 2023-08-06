from sklearn.base import BaseEstimator, TransformerMixin


class ProbaTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, model, drop=True):
        self.model = model
        self.drop = drop

    def fit(self, *args, **kwargs):
        self.model.fit(*args, **kwargs)
        return self

    def transform(self, X, **transform_params):
        Xtrans = self.model.predict_proba(X)
        if self.drop:
            Xtrans = Xtrans[:, 1:]
        return Xtrans
