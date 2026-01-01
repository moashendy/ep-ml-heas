import numpy as np
import pandas as pd

def add_temperature_features(df):
    df = df.copy()

    #  Basic checks
    required = ["T_e", "C_e", "tau_e", "k_e", "k_lat"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Temperature scaling
    df["logT"] = np.log10(df["T_e"])
    
    if "Debye_T" in df.columns:
        df["T_norm"] = df["T_e"] / df["Debye_T"]
    else:
        df["T_norm"] = df["T_e"]  # fallback

    # Physics-informed combinations
    df["Ce_over_T"] = df["C_e"] / df["T_e"]
    df["T_tau"] = df["T_e"] * df["tau_e"]
    df["k_ratio"] = df["k_e"] / (df["k_lat"] + 1e-6)

    return df
