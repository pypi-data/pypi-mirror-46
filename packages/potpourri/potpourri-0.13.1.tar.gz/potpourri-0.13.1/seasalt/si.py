# For Univariate Regression
from sklearn.metrics import (
    make_scorer, r2_score,
    explained_variance_score, mean_absolute_error, mean_squared_error,
    mean_squared_log_error, median_absolute_error)

# Create Scorer - Ensure the lowest value means "best"
scorerfun = r2_score

# Hyperparameter Optimization settings
cv_settings = {
    'n_iter': 50,  # How many random hyperparmeter settings to try
    'cv': 5,  # Number of CV folds
    'scoring': make_scorer(scorerfun),
    'random_state': 42,
    'n_jobs': -1,
    'return_train_score': True
}


# Evaluate by watching some metrics
def print_scores(y_true, y_pred):
    """
    Y_pred = model.predict(X_valid)
    print_scores(Y_valid, Y_pred)
    """
    print("{:>20s}: {:12.4f}".format(
        "Mean Squared Error", mean_squared_error(y_true, y_pred)))
    print("{:>20s}: {:12.4f}".format(
        "Mean Absolute Error", mean_absolute_error(y_true, y_pred)))
    print("{:>20s}: {:12.4f}".format(
        "Median Abs Error", median_absolute_error(y_true, y_pred)))
    # print("{:>20s}: {:12.4f}".format(
    #    "Mean Sq Log Error", mean_squared_log_error(y_true, y_pred)))
    print("{:>20s}: {:12.4f}".format(
        "R Squared", r2_score(y_true, y_pred)))
    print("{:>20s}: {:12.4f}".format(
        "Explained Variance", explained_variance_score(y_true, y_pred)))
