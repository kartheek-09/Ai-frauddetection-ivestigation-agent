import os, json, joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score, classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

DATA = "data/transactions.csv"
MODEL = "models/fraud_model.joblib"
META = "models/model_metadata.json"

NUM = ["amount","transaction_hour","distance_from_usual_location",
       "device_risk_score","location_risk_score",
       "previous_failed_transactions","previous_fraud_history",
       "recent_transaction_count","account_age_days"]
CAT = ["merchant_category","payment_method"]

df = pd.read_csv(DATA)
X, y = df[NUM+CAT], df["is_fraud"]
Xtr, Xte, ytr, yte = train_test_split(X,y,test_size=.2,stratify=y,random_state=42)

pre = ColumnTransformer([
    ("num", SimpleImputer(strategy="median"), NUM),
    ("cat", Pipeline([("imp",SimpleImputer(strategy="most_frequent")),
                      ("enc",OneHotEncoder(handle_unknown="ignore"))]), CAT)
])

models = {
    "logistic_regression": LogisticRegression(max_iter=1000,class_weight="balanced"),
    "random_forest": RandomForestClassifier(n_estimators=150,max_depth=8,
                                             class_weight="balanced",random_state=42)
}

best, best_auc, best_name = None, -1, None
results = {}

for name, model in models.items():
    pipe = Pipeline([("preprocessor",pre),("model",model)])
    pipe.fit(Xtr,ytr)
    p = pipe.predict_proba(Xte)[:,1]
    pred = (p >= .5).astype(int)
    auc = roc_auc_score(yte,p)
    results[name] = {"roc_auc":float(auc),
                     "pr_auc":float(average_precision_score(yte,p))}
    print("\n",name, "ROC-AUC:", round(auc,4),
          "PR-AUC:", round(results[name]["pr_auc"],4))
    print(classification_report(yte,pred))
    if auc > best_auc:
        best,best_auc,best_name = pipe,auc,name

os.makedirs("models",exist_ok=True)
joblib.dump(best,MODEL)
with open(META,"w") as f:
    json.dump({"model":best_name,"roc_auc":best_auc,"features":NUM+CAT,"results":results},f,indent=2)
print("\nSaved:", MODEL)
