import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression


def train_baseline_models(df, target="target", random_state=42):
    """
    Train simple baseline models on HEA descriptors.

    Parameters
    ----------
    df : pandas.DataFrame
        Feature dataframe containing descriptors and target.
    target : str
        Name of target column.
    random_state : int

    Returns
    -------
    results : dict
        Model performance metrics.
    """

    # -----------------------
    # 1. Feature selection
    # -----------------------
    feature_cols = [
        "VEC",
        "delta",
        "chi_avg",
    ]

    X = df[feature_cols]
    y = df[target]

    # -----------------------
    # 2. Train / test split
    # -----------------------
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state
    )

    results = {}

    # -----------------------
    # 3. Linear Regression
    # -----------------------
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)

    results["LinearRegression"] = {
        "R2": r2_score(y_test, y_pred),
        "MAE": mean_absolute_error(y_test, y_pred),
    }

    # -----------------------
    # 4. Random Forest
    # -----------------------
    rf = RandomForestRegressor(
        n_estimators=200,
        random_state=random_state
    )
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)

    results["RandomForest"] = {
        "R2": r2_score(y_test, y_pred),
        "MAE": mean_absolute_error(y_test, y_pred),
    }

    return results
