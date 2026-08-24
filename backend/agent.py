def investigate(t, prediction):
    p = prediction["fraud_probability"]
    risk = "HIGH" if p >= .75 else "MEDIUM" if p >= .35 else "LOW"
    factors = []
    if t["device_risk_score"] >= .75: factors.append("High device risk")
    if t["location_risk_score"] >= .75: factors.append("High location risk")
    if t["distance_from_usual_location"] >= 200: factors.append("Large location deviation")
    if t["previous_fraud_history"] == 1: factors.append("Previous fraud history")
    if t["previous_failed_transactions"] >= 3: factors.append("Multiple failed transactions")
    if t["transaction_hour"] < 5: factors.append("Unusual transaction time")
    if t["amount"] >= 20000: factors.append("High transaction amount")

    if risk == "HIGH" and len(factors) >= 2:
        decision, action = "BLOCK", "Block transaction and request additional verification."
    elif risk == "HIGH":
        decision, action = "REVIEW", "Send transaction for manual review."
    elif risk == "MEDIUM":
        decision, action = "REVIEW", "Request additional verification before approval."
    else:
        decision, action = "APPROVE", "Approve transaction while continuing normal monitoring."

    summary = ("The investigation identified: " + ", ".join(factors) + "."
               if factors else "No major rule-based risk indicators were identified.")
    return {"risk_level":risk,"decision":decision,"top_risk_factors":factors,
            "recommended_action":action,"investigation_summary":summary,
            "confidence":round(max(p,1-p),4)}
