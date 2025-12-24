import re
import pandas as pd

ELEMENTS = ["Al", "Cr", "Fe", "Co", "Ni", "Mn", "Cu"]
# Elemental properties (literature values)
VEC = {
    "Al": 3, "Cr": 6, "Fe": 8, "Co": 9,
    "Ni": 10, "Mn": 7, "Cu": 11
}

ATOMIC_RADIUS = {  # metallic radius in Å
    "Al": 1.43, "Cr": 1.28, "Fe": 1.26, "Co": 1.25,
    "Ni": 1.24, "Mn": 1.27, "Cu": 1.28
}

ELECTRONEGATIVITY = {  # Pauling
    "Al": 1.61, "Cr": 1.66, "Fe": 1.83, "Co": 1.88,
    "Ni": 1.91, "Mn": 1.55, "Cu": 1.90
}

def parse_composition_string(comp):
    fractions = {el: 0.0 for el in ELEMENTS}

    # Case 1: Equiatomic like AlCrFeCoNi
    if "-" not in comp and "_" not in comp:
        els = re.findall(r"[A-Z][a-z]?", comp)
        frac = 1.0 / len(els)
        for el in els:
            fractions[el] = frac
        return fractions

    # Case 2: Explicit like Co-0.05_Xx3-0.95
    parts = comp.split("_")
    remaining_frac = 0.0
    remaining_elements = []

    for p in parts:
        if "Xx" in p:
            n = int(re.search(r"Xx(\d+)", p).group(1))
            remaining_frac = float(p.split("-")[1])
            remaining_elements = n
        else:
            el, val = p.split("-")
            fractions[el] = float(val)

    # Assign remaining fraction equally
    unspecified = [el for el in ELEMENTS if fractions[el] == 0]
    if remaining_frac > 0 and len(unspecified) > 0:
        for el in unspecified[:remaining_elements]:
            fractions[el] = remaining_frac / remaining_elements

    return fractions


def expand_compositions(df):
    rows = []
    for _, row in df.iterrows():
        comp = row["Composition"]
        frac = parse_composition_string(comp)
        for el, v in frac.items():
            row[el] = v
        rows.append(row)

    return pd.DataFrame(rows)

def compute_VEC(row):
    return sum(row[e] * VEC[e] for e in VEC if e in row)

def compute_avg_radius(row):
    return sum(row[e] * ATOMIC_RADIUS[e] for e in ATOMIC_RADIUS if e in row)

def compute_delta(row):
    r_bar = compute_avg_radius(row)
    return 100 * (sum(
        row[e] * (1 - ATOMIC_RADIUS[e] / r_bar) ** 2
        for e in ATOMIC_RADIUS if e in row
    ) ** 0.5)

def compute_avg_electronegativity(row):
    return sum(row[e] * ELECTRONEGATIVITY[e] for e in ELECTRONEGATIVITY if e in row)

