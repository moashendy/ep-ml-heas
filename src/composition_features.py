import re
import pandas as pd

ELEMENTS = ["Al", "Cr", "Fe", "Co", "Ni", "Mn", "Cu"]

def parse_composition(comp):
    """
    Convert composition string into elemental fractions.
    """

    fractions = dict.fromkeys(ELEMENTS, 0.0)

    # Case 1: Equiatomic HEA (e.g. AlCrFeCoNi)
    if "-" not in comp:
        elems = re.findall(r"[A-Z][a-z]?", comp)
        frac = 1.0 / len(elems)
        for e in elems:
            fractions[e] = frac
        return fractions

    # Case 2: Perturbation alloy (e.g. Co-0.05_Xx3-0.95)
    main_elem, rest = comp.split("_")
    elem, x_elem = main_elem.split("-")
    x_elem = float(x_elem)

    fractions[elem] = x_elem

    # Extract how many elements share the remainder
    m = re.search(r"Xx(\d+)-([\d.]+)", rest)
    n_rest = int(m.group(1))
    x_rest = float(m.group(2))

    remaining_elements = [e for e in ELEMENTS if e != elem and e in comp or e in ["Cr","Fe","Ni"]]

    # For your dataset, the base system is CrFeNi
    base = ["Cr", "Fe", "Ni"]

    share = x_rest / len(base)
    for e in base:
        fractions[e] = share

    return fractions


def expand_compositions(df):
    comp_features = df["Composition"].apply(parse_composition)
    comp_df = pd.DataFrame(comp_features.tolist())
    return pd.concat([df.drop(columns=["Composition"]), comp_df], axis=1)
