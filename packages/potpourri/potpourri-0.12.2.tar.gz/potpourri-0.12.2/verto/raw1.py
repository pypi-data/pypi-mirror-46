from mlxtend.preprocessing import CopyTransformer

trans = CopyTransformer()

meta = {
    'id': 'raw1',
    'name': 'Raw Features',
    'description': (
        "Just copy raw features to comply with "
        "this preprocessing framewortk."),
    'keywords': ['CopyTransformer', 'mlxtend'],
    'feature_names_prefix': 'raw'
}
