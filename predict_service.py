# predict_service.py
import os
import pandas as pd
import numpy as np
import json
import joblib
from tensorflow.keras.models import load_model

# Disable GPU
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

BASE_DIR = os.path.dirname(__file__)
model = None
scaler = None
X_columns = None
num_cols = None

def load_model_objects():
    global model, scaler, X_columns, num_cols
    model = load_model(os.path.join(BASE_DIR, "mental_wellness_model.keras"))
    scaler = joblib.load(os.path.join(BASE_DIR, "scaler.joblib"))
    with open(os.path.join(BASE_DIR, "columns.json"), "r") as f:
        info = json.load(f)
    X_columns = info["X_columns"]
    num_cols = info["num_cols"]

def predict_new_user(new_user_dict):
    global model, scaler, X_columns, num_cols
    if model is None:
        load_model_objects()
    new_user_df = pd.DataFrame([new_user_dict])
    cat_cols = ['gender', 'occupation', 'work_mode']
    new_user_df = pd.get_dummies(new_user_df, columns=cat_cols, drop_first=True)

    for col in X_columns:
        if col not in new_user_df.columns:
            new_user_df[col] = 0

    new_user_df = new_user_df[X_columns]
    new_user_df[num_cols] = scaler.transform(new_user_df[num_cols])
    prediction = model.predict(new_user_df)[0][0]
    return float(np.clip(prediction, 0, 100))
