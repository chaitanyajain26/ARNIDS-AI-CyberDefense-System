import pandas as pd
import numpy as np
import os

print("\n[INFO] Starting Data Preprocessing...")


# FOLDER PATH

folder_path = "data/raw/csv/"

all_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

print("[INFO] Files Found:", all_files)


# LOAD & MERGE

df_list = []

for file in all_files:
    file_path = os.path.join(folder_path, file)
    print("[INFO] Loading:", file)

    temp_df = pd.read_csv(file_path)

    df_list.append(temp_df)

df = pd.concat(df_list, ignore_index=True)

print("[INFO] Total Shape:", df.shape)


# CLEAN DATA


# Replace infinity
df = df.replace([np.inf, -np.inf], np.nan)

# Drop NaN
df = df.dropna()

print("[INFO] After Cleaning:", df.shape)


# SAVE CLEAN DATA

os.makedirs("data/processed", exist_ok=True)

output_path = "data/processed/clean_data.csv"
df.to_csv(output_path, index=False)

print("\n[INFO] Clean Data Saved at:", output_path)