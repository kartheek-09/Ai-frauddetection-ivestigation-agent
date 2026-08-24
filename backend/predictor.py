import os, joblib, pandas as pd
from backend.config import MODEL_PATH

_model = None

def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("Model missing. Run: python training/train.py")
        _model = joblib.load(MODEL_PATH)
    return _model

def predict(data):
    p = float(get_model().predict_proba(pd.DataFrame([data]))[0,1])
    return {"fraud_probability":round(p,4),
            "prediction":"FRAUD" if p >= .5 else "LEGITIMATE"}
