from sklearn.linear_model import LinearRegression, Ridge
from sklearn.svm import SVR
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor


def get_models(random_state=42):
    """
    Returns a dictionary of regression models for benchmarking.
    """
    models = {
        "Linear": LinearRegression(),
        "Ridge": Ridge(alpha=1.0),
        "SVR": SVR(C=10, epsilon=0.1),
        "GBR": GradientBoostingRegressor(random_state=random_state),
        "RF": RandomForestRegressor(
            n_estimators=300,
            random_state=random_state,
            n_jobs=-1
        )
    }

    return models
