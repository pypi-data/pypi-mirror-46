

def create_feature_names(prefix, n_features):
    """Generate numbered feature names

    Example
    -------
        from seasalt import create_feature_names
        from verto.dim1 import trans, meta
        from datasets.demo1 import X_train

        trans.set_params(**{'pca__n_components': 3})
        X_new = trans.fit_transform(X_train)
        names = create_feature_names(
            meta['feature_names_prefix'], X_new.shape[1])
        print(names)

        import pandas as pd
        df = pd.DataFrame(data=X_new, columns=names)
        df
    """
    return [prefix + "_" + str(i) for i in range(n_features)]
