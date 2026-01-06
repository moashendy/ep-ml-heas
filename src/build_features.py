import pandas as pd
import sys
import os

sys.path.append(os.path.abspath("../src"))

from composition_features import expand_compositions
from alloy_descriptors import compute_alloy_descriptors, VEC


RAW_FILE = "../data/processed/master_hea_data.csv"
OUTPUT_FILE = "../data/processed/master_hea_features.csv"


if os.path.exists(RAW_FILE):
    df = pd.read_csv(RAW_FILE)
    print(f"Loaded: {RAW_FILE}")

    # Expand compositions into elemental fractions
    df = expand_compositions(df)
    print("Expanded compositions")

    # Identify valid element columns using VEC dictionary
    elements = [el for el in VEC.keys() if el in df.columns]
    print(f"Elements detected: {elements}")

    # Compute alloy descriptors
    df = compute_alloy_descriptors(df, elements)
    print("Computed alloy descriptors (VEC, delta, chi_avg)")

    # Temperature-derived features
    if "T_e" in df.columns:
        df["T_norm"] = df["T_e"] / df["T_e"].max()
        df["T_sq"] = df["T_norm"] ** 2
        df["T_VEC"] = df["T_norm"] * df["VEC"]
        print("Added temperature features")
    else:
        print("Warning: 'T_e' not found. Temperature features skipped.")

    # Save features
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved features to {OUTPUT_FILE}")

else:
    print(f"Error: File not found at {RAW_FILE}")
