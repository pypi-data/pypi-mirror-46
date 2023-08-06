from sklearn.preprocessing import QuantileTransformer


trans = QuantileTransformer(
    n_quantiles = 512,
    output_distribution = 'uniform'  # uniform, normal
)

meta = {
    'id': 'scl1',
    'name': 'Quantile Scaler',
    'description': (
        "Transform data to by its percentiles to "
        "an uniform distribution"),
    'keywords': [
        'QuantileTransformer', 'probability density'],
    'feature_names_prefix': 'scl_qntl'
}
