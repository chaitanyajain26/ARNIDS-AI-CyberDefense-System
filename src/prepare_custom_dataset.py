"""
ARNIDS - AI Powered Adversarial Robust Network Intrusion Detection System

Developed by: Chaitanya Jain
GitHub: https://github.com/chaitanyajain26

Copyright (c) 2026 Chaitanya Jain

Licensed under the MIT License.
"""


import pandas as pd
import numpy as np
import os

print("\n[INFO] Creating Custom Dataset...")

folder_path = "data/raw/csv/"

all_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

df_list = []

for file in all_files:
    print("[INFO] Loading:", file)
    file_path = os.path.join(folder_path, file)

    df = pd.read_csv(file_path, encoding='latin1')
    df.columns = df.columns.str.strip()

    temp = pd.DataFrame()

    # =========================
    # SAFE FEATURE EXTRACTION
    # =========================

    # total packets
    if 'Total Fwd Packets' in df.columns and 'Total Backward Packets' in df.columns:
        temp['total_packets'] = df['Total Fwd Packets'] + df['Total Backward Packets']
    else:
        temp['total_packets'] = 0

    # avg packet size
    if 'Packet Length Mean' in df.columns:
        temp['avg_packet_size'] = df['Packet Length Mean']
    else:
        temp['avg_packet_size'] = 0

    # max packet size
    if 'Max Packet Length' in df.columns:
        temp['max_packet_size'] = df['Max Packet Length']
    else:
        temp['max_packet_size'] = 0

    # protocol 
    if 'Protocol' in df.columns:
        temp['protocol_count'] = df['Protocol']
    elif 'Protocol ID' in df.columns:
        temp['protocol_count'] = df['Protocol ID']
    else:
        temp['protocol_count'] = 0

    # label
    if 'Label' in df.columns:
        temp['Label'] = df['Label']
    else:
        print("[WARNING] Label column missing in", file)
        continue

    df_list.append(temp)


# MERGE ALL

final_df = pd.concat(df_list, ignore_index=True)

# CLEAN
final_df = final_df.replace([np.inf, -np.inf], np.nan)
final_df = final_df.dropna()

# SAVE
os.makedirs("data/processed", exist_ok=True)

final_df.to_csv("data/processed/custom_data.csv", index=False)

print("\n[INFO] Custom dataset created!")
print("[INFO] Shape:", final_df.shape)