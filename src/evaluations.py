import numpy as np
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.model_selection import GroupKFold


def evaluate_model(model, X, y, groups, n_splits=5):
    """
    Evaluate a regression model using GroupKFold cross-validation.
    """
    gkf = GroupKFold(n_splits=n_splits)

    r2s, maes = [], []

    for train_idx, test_idx in gkf.split(X, y, groups):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        r2s.append(r2_score(y_test, y_pred))
        maes.append(mean_absolute_error(y_test, y_pred))

    return {
        "r2_mean": np.mean(r2s),
        "r2_std": np.std(r2s),
        "mae_mean": np.mean(maes)
    }


def crossval_predictions(model, X, y, groups, n_splits=5):
    """
    Returns out-of-fold predictions for parity plots.
    """
    gkf = GroupKFold(n_splits=n_splits)

    y_true_all = []
    y_pred_all = []

    for train_idx, test_idx in gkf.split(X, y, groups):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        y_true_all.extend(y_test.values)
        y_pred_all.extend(y_pred)

    return np.array(y_true_all), np.array(y_pred_all)