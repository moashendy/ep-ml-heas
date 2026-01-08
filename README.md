Physics-Aware Machine Learning for High-Entropy Alloys (HEAs)

This project develops physics-informed machine learning models to predict the electron heat capacity (Cₑ) of high-entropy alloys (HEAs) using first-principles simulation data.
The workflow combines composition-based alloy descriptors, temperature-aware physical features, and group-aware cross-validation to ensure robust generalization across alloy systems.

 Scientific Motivation

Thermophysical properties such as electron heat capacity (Cₑ) play a critical role in:

Thermal transport

Ultrafast laser–matter interactions

Energy and extreme-environment materials design

However, first-principles calculations of these properties are computationally expensive, especially across wide temperature and composition spaces.
This project demonstrates how machine learning can accurately reproduce first-principles trends while respecting known physical constraints.

 Data Pipeline

A custom ETL (Extract–Transform–Load) pipeline is implemented in src/:

Scans raw first-principles simulation outputs.

Extracts alloy composition metadata using regular expressions.

Aggregates temperature-dependent simulation data into a unified master dataset.

Produces a clean, reproducible ML-ready dataset in data/processed/.

This design ensures traceability, reproducibility, and extensibility.

 Feature Engineering
Composition-Based Alloy Descriptors (Temperature Invariant)

Computed strictly from composition:

VEC – Valence Electron Concentration

δ – Atomic size mismatch (lattice distortion descriptor)

χ̄ – Average electronegativity

These descriptors are validated to be constant across temperature, preventing data leakage.

 Machine Learning Models

The following regression models are evaluated:

Linear Regression

Ridge Regression

Support Vector Regression (SVR)

Random Forest (RF)

Gradient Boosting Regressor (GBR)

Validation Strategy

GroupKFold cross-validation, grouped by alloy composition

Ensures no temperature points from the same alloy appear in both train and test sets

Tests true generalization to unseen alloys

 Results (Target: Electron Heat Capacity, Cₑ)
Model	R² (mean ± std)	MAE
Linear	0.958 ± 0.038	42.3
Ridge	0.916 ± 0.065	57.2
SVR	0.940 ± 0.043	48.7
GBR	0.963 ± 0.038	24.4
RF	0.961 ± 0.037	24.6

Key observations:

Nonlinear models outperform linear baselines.

Performance is consistent across folds, indicating stable generalization.

Errors are physically reasonable given the wide temperature range.

 Model Interpretability

Feature importance analysis reveals:

Temperature-related features dominate, consistent with the physical definition of Cₑ.

Composition descriptors (δ, VEC, χ̄) provide secondary but meaningful corrections.

Alloy chemistry modulates temperature-driven behavior rather than replacing it.

This confirms that the model is learning physics-informed trends, not spurious correlations.

 Visualizations

Parity plots comparing predicted vs. first-principles Cₑ values

Feature importance rankings

Correlation analysis and ablation studies

All plots and raw data used to generate them are stored in results/.

 Why This Project Matters

Demonstrates physics-aware ML, not black-box fitting

Uses proper cross-validation for materials data

Fully reproducible and extensible

Directly relevant to:

Computational materials science

Energy materials

Thermal transport modeling

Data-driven alloy design


 Author
Mohamed Hendy
