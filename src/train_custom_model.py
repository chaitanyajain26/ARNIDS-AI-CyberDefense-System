import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

print("\n[INFO] Training Custom Model...")

# LOAD DATA

file_path = "data/processed/custom_data.csv"

if not os.path.exists(file_path):
    print("[ERROR] Dataset not found!")
    exit()

df = pd.read_csv(file_path)

print("[INFO] Dataset Loaded:", df.shape)


# CLEAN

df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna()


# FEATURES

X = df[['total_packets', 'avg_packet_size', 'max_packet_size', 'protocol_count']]
y = df['Label'].astype(str)

# REDUCE SIZE (FAST TRAIN)

if len(df) > 200000:
    print("[INFO] Reducing dataset size...")
    df = df.sample(200000, random_state=42)
    X = df[['total_packets', 'avg_packet_size', 'max_packet_size', 'protocol_count']]
    y = df['Label']


# SPLIT

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


# SCALE

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# MODEL

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)


# SAVE

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/custom_model.pkl")
joblib.dump(scaler, "models/custom_scaler.pkl")

print("[INFO] Custom Model Saved Successfully!")