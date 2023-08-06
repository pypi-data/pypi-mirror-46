# For Single-Output Binary Classification

# Create Scorer - Ensure the highest value means "best"
import korr
from sklearn.metrics import (
    make_scorer,
    balanced_accuracy_score, hamming_loss, jaccard_similarity_score,
    precision_score, recall_score, matthews_corrcoef)


def scorerfun(y_true, y_pred):
    return korr.confusion_to_mcc(*korr.confusion(y_true, y_pred).ravel())


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
    print("{:>20s}: {:8.6f}".format(
        "Matthews", matthews_corrcoef(y_true, y_pred)))
    print("{:>20s}: {:8.6f}".format(
        "Accurancy", balanced_accuracy_score(y_true, y_pred)))
    print("{:>20s}: {:8.6f}".format(
        "Jaccard", jaccard_similarity_score(y_true, y_pred)))
    print("{:>20s}: {:8.6f}".format(
        "Hamming", hamming_loss(y_true, y_pred)))
    print("{:>20s}: {:8.6f}".format(
        "Precision", precision_score(y_true, y_pred)))
    print("{:>20s}: {:8.6f}".format(
        "Recall", recall_score(y_true, y_pred)))
