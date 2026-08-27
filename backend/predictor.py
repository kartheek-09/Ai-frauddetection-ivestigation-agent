import os
import json
import joblib
import pandas as pd

from backend.config import MODEL_PATH


_model = None
_threshold = 0.5


def get_model():
    global _model, _threshold

    if _model is None:

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                "Model missing. Run: python training/train.py"
            )

        _model = joblib.load(MODEL_PATH)

        metadata_path = os.path.join(
            os.path.dirname(MODEL_PATH),
            "model_metadata.json"
        )

        if os.path.exists(metadata_path):

            try:
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)

                _threshold = float(
                    metadata.get(
                        "decision_threshold",
                        0.5
                    )
                )

            except (json.JSONDecodeError, ValueError, TypeError):
                _threshold = 0.5

    return _model


def predict(data):

    model = get_model()

    probability = float(
        model.predict_proba(
            pd.DataFrame([data])
        )[0, 1]
    )

    prediction = (
        "FRAUD"
        if probability >= _threshold
        else "LEGITIMATE"
    )

    return {
        "fraud_probability": round(
            probability,
            4
        ),
        "prediction": prediction,
        "decision_threshold": _threshold
    }