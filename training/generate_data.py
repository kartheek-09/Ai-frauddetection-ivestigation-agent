import os
import numpy as np
import pandas as pd

os.makedirs("data", exist_ok=True)
rng = np.random.default_rng(42)
n = 3000

amount = np.round(rng.lognormal(7.0, 1.0, n), 2)
hour = rng.integers(0, 24, n)
distance = np.round(rng.exponential(80, n), 2)
device = np.round(rng.random(n), 3)
location = np.round(rng.random(n), 3)
failed = rng.poisson(0.7, n)
prev_fraud = rng.binomial(1, 0.04, n)
recent = rng.poisson(4, n)
account_age = rng.integers(10, 2000, n)
merchant = rng.choice(["grocery","electronics","travel","fashion","gaming"], n)
payment = rng.choice(["card","upi","netbanking"], n)

score = (-4.2 + 0.000025*amount + 1.3*device + 1.2*location
         + 0.35*failed + 2.0*prev_fraud + 0.10*recent
         + 0.7*(hour < 5) + 0.004*distance - 0.00015*account_age)
prob = 1/(1+np.exp(-score))
fraud = rng.binomial(1, np.clip(prob, 0.01, 0.90))

df = pd.DataFrame({
    "amount": amount, "transaction_hour": hour,
    "distance_from_usual_location": distance,
    "device_risk_score": device, "location_risk_score": location,
    "previous_failed_transactions": failed,
    "previous_fraud_history": prev_fraud,
    "recent_transaction_count": recent,
    "account_age_days": account_age,
    "merchant_category": merchant, "payment_method": payment,
    "is_fraud": fraud
})
df.to_csv("data/transactions.csv", index=False)
print(f"Created {len(df)} records.")
