import pandas as pd

from models import get_models
from evaluation import evaluate_model


# Load data
data = pd.read_csv("../data/processed_data.csv")

X = data.drop(columns=["C_e", "group"])
y = data["C_e"]
groups = data["group"]

# Load models
models = get_models()

# Train & evaluate
for name, model in models.items():
    results = evaluate_model(model, X, y, groups)

    print(
        f"{name:8s} | "
        f"R² = {results['r2_mean']:.3f} ± {results['r2_std']:.3f} | "
        f"MAE = {results['mae_mean']:.3f}"
    )
