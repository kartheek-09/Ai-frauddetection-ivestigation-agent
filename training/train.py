import os
import json
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier


DATA = "data/transactions.csv"
MODEL = "models/fraud_model.joblib"
META = "models/model_metadata.json"
EVALUATION = "models/evaluation.json"

NUM = [
    "amount",
    "transaction_hour",
    "distance_from_usual_location",
    "device_risk_score",
    "location_risk_score",
    "previous_failed_transactions",
    "previous_fraud_history",
    "recent_transaction_count",
    "account_age_days"
]

CAT = [
    "merchant_category",
    "payment_method"
]


FALSE_POSITIVE_COST = 500
FALSE_NEGATIVE_COST = 5000

THRESHOLDS = [
    0.30,
    0.40,
    0.50,
    0.60,
    0.70
]


df = pd.read_csv(DATA)

X = df[NUM + CAT]
y = df["is_fraud"]


Xtr, Xte, ytr, yte = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)


pre = ColumnTransformer([
    (
        "num",
        Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ]),
        NUM
    ),
    (
        "cat",
        Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore"))
        ]),
        CAT
    )
])


models = {
    "logistic_regression": LogisticRegression(
        max_iter=2000,
        class_weight="balanced"
    ),

    "random_forest": RandomForestClassifier(
        n_estimators=150,
        max_depth=8,
        class_weight="balanced",
        random_state=42
    )
}


best = None
best_auc = -1
best_name = None

results = {}


for name, model in models.items():

    pipe = Pipeline([
        ("preprocessor", pre),
        ("model", model)
    ])

    pipe.fit(Xtr, ytr)

    probability = pipe.predict_proba(Xte)[:, 1]

    auc = roc_auc_score(
        yte,
        probability
    )

    pr_auc = average_precision_score(
        yte,
        probability
    )

    print("\n" + "=" * 60)
    print(name.upper())
    print("=" * 60)

    print("ROC-AUC:", round(auc, 4))
    print("PR-AUC:", round(pr_auc, 4))

    threshold_results = {}

    for threshold in THRESHOLDS:

        prediction = (
            probability >= threshold
        ).astype(int)

        precision = precision_score(
            yte,
            prediction,
            zero_division=0
        )

        recall = recall_score(
            yte,
            prediction,
            zero_division=0
        )

        f1 = f1_score(
            yte,
            prediction,
            zero_division=0
        )

        tn, fp, fn, tp = confusion_matrix(
            yte,
            prediction
        ).ravel()

        false_positive_rate = (
            fp / (fp + tn)
            if (fp + tn) > 0
            else 0
        )

        false_negative_rate = (
            fn / (fn + tp)
            if (fn + tp) > 0
            else 0
        )

        fp_cost = (
            fp * FALSE_POSITIVE_COST
        )

        fn_cost = (
            fn * FALSE_NEGATIVE_COST
        )

        total_cost = (
            fp_cost + fn_cost
        )

        threshold_key = str(threshold)

        threshold_results[threshold_key] = {
            "threshold": threshold,
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1_score": round(float(f1), 4),
            "false_positive_rate": round(
                float(false_positive_rate),
                4
            ),
            "false_negative_rate": round(
                float(false_negative_rate),
                4
            ),
            "true_negatives": int(tn),
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "true_positives": int(tp),
            "false_positive_cost": int(fp_cost),
            "false_negative_cost": int(fn_cost),
            "total_estimated_cost": int(total_cost)
        }

        print(
            f"Threshold {threshold:.2f} | "
            f"Precision: {precision:.4f} | "
            f"Recall: {recall:.4f} | "
            f"F1: {f1:.4f} | "
            f"FP: {fp} | "
            f"FN: {fn} | "
            f"Cost: ₹{total_cost:,}"
        )

    results[name] = {
        "roc_auc": round(float(auc), 4),
        "pr_auc": round(float(pr_auc), 4),
        "thresholds": threshold_results
    }

    if auc > best_auc:
        best = pipe
        best_auc = auc
        best_name = name


best_threshold_data = results[best_name]["thresholds"]

best_threshold_key = min(
    best_threshold_data,
    key=lambda x: best_threshold_data[x][
        "total_estimated_cost"
    ]
)

best_threshold = best_threshold_data[
    best_threshold_key
]

selected_threshold = best_threshold[
    "threshold"
]


# Final evaluation using selected threshold

final_probability = best.predict_proba(Xte)[:, 1]

final_prediction = (
    final_probability >= selected_threshold
).astype(int)

final_precision = precision_score(
    yte,
    final_prediction,
    zero_division=0
)

final_recall = recall_score(
    yte,
    final_prediction,
    zero_division=0
)

final_f1 = f1_score(
    yte,
    final_prediction,
    zero_division=0
)

final_auc = roc_auc_score(
    yte,
    final_probability
)

final_pr_auc = average_precision_score(
    yte,
    final_probability
)

tn, fp, fn, tp = confusion_matrix(
    yte,
    final_prediction
).ravel()

final_fpr = (
    fp / (fp + tn)
    if (fp + tn) > 0
    else 0
)

final_fnr = (
    fn / (fn + tp)
    if (fn + tp) > 0
    else 0
)

final_fp_cost = (
    fp * FALSE_POSITIVE_COST
)

final_fn_cost = (
    fn * FALSE_NEGATIVE_COST
)

final_total_cost = (
    final_fp_cost + final_fn_cost
)


print("\n" + "=" * 60)
print("SELECTED MODEL")
print("=" * 60)

print("Model:", best_name)
print("Decision Threshold:", selected_threshold)
print("ROC-AUC:", round(final_auc, 4))
print("PR-AUC:", round(final_pr_auc, 4))
print("Precision:", round(final_precision, 4))
print("Recall:", round(final_recall, 4))
print("F1 Score:", round(final_f1, 4))
print("False Positive Rate:", round(final_fpr, 4))
print("False Negative Rate:", round(final_fnr, 4))
print("False Positives:", fp)
print("False Negatives:", fn)
print("Estimated Business Cost:", f"₹{final_total_cost:,}")

print("\nClassification Report:")

print(
    classification_report(
        yte,
        final_prediction,
        zero_division=0
    )
)

print("Confusion Matrix:")

print(
    confusion_matrix(
        yte,
        final_prediction
    )
)


os.makedirs(
    "models",
    exist_ok=True
)


joblib.dump(
    best,
    MODEL
)


metadata = {
    "model": best_name,
    "roc_auc": round(float(final_auc), 4),
    "pr_auc": round(float(final_pr_auc), 4),
    "decision_threshold": selected_threshold,
    "features": NUM + CAT,
    "training_samples": int(len(Xtr)),
    "test_samples": int(len(Xte)),
    "test_size": 0.20,
    "random_state": 42,
    "results": results
}


with open(
    META,
    "w"
) as f:
    json.dump(
        metadata,
        f,
        indent=2
    )


evaluation = {
    "project": "AI Fraud Detection & Investigation Agent",

    "track": "Track 02 - AI Risk Manager",

    "dataset": {
        "type": "synthetic",
        "total_records": int(len(df)),
        "training_records": int(len(Xtr)),
        "test_records": int(len(Xte))
    },

    "best_model": best_name,

    "held_out_test_metrics": {
        "precision": round(float(final_precision), 4),
        "recall": round(float(final_recall), 4),
        "f1_score": round(float(final_f1), 4),
        "roc_auc": round(float(final_auc), 4),
        "pr_auc": round(float(final_pr_auc), 4)
    },

    "decision_threshold": selected_threshold,

    "confusion_matrix": {
        "true_negatives": int(tn),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "true_positives": int(tp)
    },

    "error_rates": {
        "false_positive_rate": round(
            float(final_fpr),
            4
        ),
        "false_negative_rate": round(
            float(final_fnr),
            4
        )
    },

    "business_cost": {
        "false_positive_cost_per_case":
            FALSE_POSITIVE_COST,

        "false_negative_cost_per_case":
            FALSE_NEGATIVE_COST,

        "estimated_false_positive_cost":
            int(final_fp_cost),

        "estimated_false_negative_cost":
            int(final_fn_cost),

        "total_estimated_cost":
            int(final_total_cost),

        "note": (
            "Cost values are assumptions for "
            "demonstration and do not represent "
            "real merchant losses."
        )
    },

    "threshold_analysis": results[best_name]["thresholds"],

    "evaluation_note": (
        "Metrics are measured on a held-out 20% "
        "test set from a synthetic transaction dataset."
    )
}


with open(
    EVALUATION,
    "w"
) as f:
    json.dump(
        evaluation,
        f,
        indent=2
    )


print("\n" + "=" * 60)
print("TRAINING COMPLETED")
print("=" * 60)

print("Best Model:", best_name)
print("Selected Threshold:", selected_threshold)
print("Precision:", round(final_precision, 4))
print("Recall:", round(final_recall, 4))
print("F1 Score:", round(final_f1, 4))
print("ROC-AUC:", round(final_auc, 4))
print("False Positives:", fp)
print("False Negatives:", fn)
print("Estimated Business Cost:", f"₹{final_total_cost:,}")

print("\nSaved:")
print(MODEL)
print(META)
print(EVALUATION)