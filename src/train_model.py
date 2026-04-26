"""
ARNIDS - AI Powered Adversarial Robust Network Intrusion Detection System

Developed by: Chaitanya Jain
GitHub: https://github.com/chaitanyajain26

Copyright (c) 2026 Chaitanya Jain

Licensed under the MIT License.
"""

import pandas as pd
import numpy as np
import joblib
import os
import sys

# FIX ENCODING ISSUE
sys.stdout.reconfigure(encoding='utf-8')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

print("\n[INFO] Starting Model Training...")


# LOAD DATA

file_path = "data/processed/clean_data.csv"

df = pd.read_csv(file_path)

# CLEAN COLUMN NAMES
df.columns = df.columns.str.strip()

print("[INFO] Dataset Loaded:", df.shape)


# CLEAN DATA

df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna()


# CHECK LABEL

if 'Label' not in df.columns:
    print("[ERROR] Label column not found!")
    print(df.columns)
    exit()


# REDUCE SIZE 

if len(df) > 200000:
    print("[INFO] Reducing dataset for faster training...")
    df = df.sample(200000, random_state=42)


# FEATURES + LABEL

X = df.select_dtypes(include=[np.number])

if 'Label' in X.columns:
    X = X.drop('Label', axis=1)

y = df['Label'].astype(str).str.strip()

print("[INFO] Features Shape:", X.shape)


# SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# SCALE

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# MODEL 1: RANDOM FOREST

print("\n[INFO] Training Random Forest...")

rf_model = RandomForestClassifier(n_estimators=100)
rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)

rf_acc = accuracy_score(y_test, rf_pred)

print("[RF Accuracy]:", rf_acc)


# MODEL 2: LOGISTIC REGRESSION

print("\n[INFO] Training Logistic Regression...")

lr_model = LogisticRegression(max_iter=500)  #  increased iterations
lr_model.fit(X_train, y_train)

lr_pred = lr_model.predict(X_test)

lr_acc = accuracy_score(y_test, lr_pred)

print("[LR Accuracy]:", lr_acc)


# BEST MODEL

if rf_acc > lr_acc:
    best_model = rf_model
    model_name = "RandomForest"
    best_pred = rf_pred
else:
    best_model = lr_model
    model_name = "LogisticRegression"
    best_pred = lr_pred

print("\n[INFO] Best Model:", model_name)


# METRICS (SAFE PRINT)

try:
    print("\n[INFO] Classification Report:\n")
    print(classification_report(y_test, best_pred))
except:
    print("[WARNING] Could not print classification report (encoding issue)")

try:
    print("\n[INFO] Confusion Matrix:\n")
    print(confusion_matrix(y_test, best_pred))
except:
    print("[WARNING] Could not print confusion matrix")


# SAVE MODEL
# =========================
os.makedirs("models", exist_ok=True)

joblib.dump(best_model, "models/model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

print("\n[INFO] Model saved successfully!")