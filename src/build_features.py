import pandas as pd
import sys
import os


sys.path.append(os.path.abspath("../src"))

from composition_features import expand_compositions
from alloy_descriptors import compute_alloy_descriptors


RAW_FILE = "../data/processed/master_hea_data.csv"
OUTPUT_FILE = "../data/processed/master_hea_features.csv"


if os.path.exists(RAW_FILE):
    df = pd.read_csv(RAW_FILE)
    print(f" Loaded: {RAW_FILE}")

    # Expand compositions into fractions
    df = expand_compositions(df)
    print(" Expanded compositions")

    # Identify element columns (Assumes elements start with Uppercase letters like 'Fe', 'Ni')
    elements = [col for col in df.columns if col[0].isupper()]
    print(f"Elements detected: {elements}")

    # Compute alloy descriptors
    df = compute_alloy_descriptors(df, elements)
    print("Computed alloy descriptors (VEC, delta, chi_avg)")

    # Temperature features
    # Note: Ensure 'T_e' exists in your CSV before running this
    df['T_norm'] = df['T_e'] / df['T_e'].max()
    df['T_sq'] = df['T_norm'] ** 2
    df['T_VEC'] = df['T_norm'] * df['VEC']
    print(" Added temperature features")

    # Save the feature-enhanced dataset
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved master_hea_features.csv to {OUTPUT_FILE}")
    
    # Display the first few rows to confirm
    display(df.head())
else:
    print(f"Error: Could not find the file at {RAW_FILE}. Please check your path.")