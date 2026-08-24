from backend.config import GEMINI_API_KEY

def generate_explanation(transaction, prediction, investigation):
    if not GEMINI_API_KEY:
        return fallback(prediction, investigation)
    try:
        from google import genai
        client = genai.Client(api_key=GEMINI_API_KEY)
        prompt = f"""You are a fraud investigation assistant. Explain this transaction briefly.
Fraud probability: {prediction['fraud_probability']}
Prediction: {prediction['prediction']}
Risk: {investigation['risk_level']}
Decision: {investigation['decision']}
Risk factors: {investigation['top_risk_factors']}
Recommended action: {investigation['recommended_action']}
Do not invent facts or override the decision."""
        return client.models.generate_content(model="gemini-2.0-flash",contents=prompt).text
    except Exception:
        return fallback(prediction, investigation)

def fallback(prediction, investigation):
    return (f"Fraud probability: {prediction['fraud_probability']:.1%}. "
            f"Risk: {investigation['risk_level']}. Decision: {investigation['decision']}. "
            f"{investigation['investigation_summary']} "
            f"Recommended action: {investigation['recommended_action']}")
