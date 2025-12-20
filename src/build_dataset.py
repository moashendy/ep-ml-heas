import pandas as pd
import os
import re

def parse_filename(filename):
    """Extracts composition info from the filename."""
    # This regex looks for the part before '-First-Principles'
    match = re.search(r'^(.+?)-First-Principles', filename)
    return match.group(1) if match else "Unknown"

def process_all_files(input_dir, output_file):
    all_data = []
    
    # Get all .txt files in the raw directory
    files = [f for f in os.listdir(input_dir) if f.endswith('.txt') or 'First-Principles' in f]
    
    print(f"Found {len(files)} files.")

    cols = ["T_e", "Volume", "E_F", "N_Ef", "gamma", "C_e", "v_F", "tau_e", "k_e", "k_lat", "lambda", "Log10_Ge"]

    for f in files:
        file_path = os.path.join(input_dir, f)
        comp_name = parse_filename(f)
        
        # ... inside your loop for f in files ...
        try:
            # Read the file
            df = pd.read_csv(file_path, sep="\s+", comment='#', header=None)

            # FIX: Only keep rows where the first column is a number 
            # This removes those "N", "(E_F)", and corrupted character rows
            df = df[pd.to_numeric(df[0], errors='coerce').notnull()]
            
            # Now assign the 12 columns
            df = df.iloc[:, :12] 
            df.columns = ["T_e", "Volume", "E_F", "N_Ef", "gamma", "C_e", "v_F", "tau_e", "k_e", "k_lat", "lambda", "Log10_Ge"]
            
            # Convert all columns to float to be safe
            for col in df.columns:
                df[col] = pd.to_numeric(df[col])
                
            df['Composition'] = comp_name
            all_data.append(df)
# ...
            print(f"Successfully parsed: {comp_name}")
        except Exception as e:
            print(f"Error parsing {f}: {e}")

    # Combine all individual DataFrames into one
    master_df = pd.concat(all_data, ignore_index=True)
    
    # Save the result to the processed folder
    master_df.to_csv(output_file, index=False)
    print(f"\nSuccess! Master dataset saved to {output_file}")
    print(f"Total rows: {len(master_df)}")

if __name__ == "__main__":
    RAW_DIR = "../data/raw/"
    OUTPUT = "../data/processed/master_hea_data.csv"
    
    # Create processed directory if it doesn't exist
    os.makedirs("../data/processed/", exist_ok=True)
    
    process_all_files(RAW_DIR, OUTPUT)