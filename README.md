# Machine Learning for High-Entropy Alloys (HEAs)

This project uses First-Principles data to predict the thermophysical 
properties of alloys using Machine Learning.

## Project Structure
- `data/`: Raw and processed simulation data.
- `src/`: Python scripts for data processing and training.
- `notebooks/`: Exploratory Data Analysis and model experiments.

##  Data Pipeline
I developed a custom Python ETL (Extract, Transform, Load) pipeline located in `src/`. 
- The script scans `data/raw/` for first-principles simulation logs.
- It uses regular expressions to extract composition metadata directly from filenames and headers.
- It Aggregates individual simulations into a single master dataframe for machine learning, located in `data/processed/`.