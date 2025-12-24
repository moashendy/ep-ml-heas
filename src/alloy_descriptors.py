import numpy as np

# -----------------------------
# Elemental property tables
# -----------------------------
VEC = {
    "Al": 3, "Co": 9, "Cr": 6, "Fe": 8, "Ni": 10,
    "Mn": 7, "Ti": 4, "V": 5, "Cu": 11
}

atomic_radius = {
    "Al": 1.43, "Co": 1.25, "Cr": 1.28, "Fe": 1.26,
    "Ni": 1.24, "Mn": 1.27, "Ti": 1.47, "V": 1.34,
    "Cu": 1.28
}

electronegativity = {
    "Al": 1.61, "Co": 1.88, "Cr": 1.66, "Fe": 1.83,
    "Ni": 1.91, "Mn": 1.55, "Ti": 1.54, "V": 1.63,
    "Cu": 1.90
}

# -----------------------------
# Descriptor computation
# -----------------------------
def compute_alloy_descriptors(df, elements):
    df = df.copy()

    # Filter only elements that exist in both dataframe AND property tables
    elements = [
        el for el in elements
        if el in df.columns
    ]

    # --- VEC ---
    df["VEC"] = sum(df[el] * VEC[el] for el in elements)

    # --- Average atomic radius ---
    r_bar = sum(df[el] * atomic_radius[el] for el in elements)

    # --- Atomic size mismatch ---
    df["delta"] = np.sqrt(
        sum(df[el] * (1 - atomic_radius[el] / r_bar) ** 2 for el in elements)
    )

    # --- Average electronegativity ---
    df["chi_avg"] = sum(df[el] * electronegativity[el] for el in elements)

    return df

