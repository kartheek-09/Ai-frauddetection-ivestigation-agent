from backend.agent import investigate

def test_low_risk():
    t={"amount":1000,"transaction_hour":14,"distance_from_usual_location":5,
       "device_risk_score":.1,"location_risk_score":.1,
       "previous_failed_transactions":0,"previous_fraud_history":0}
    r=investigate(t,{"fraud_probability":.1,"prediction":"LEGITIMATE"})
    assert r["risk_level"]=="LOW"
    assert r["decision"]=="APPROVE"

def test_high_risk():
    t={"amount":50000,"transaction_hour":2,"distance_from_usual_location":500,
       "device_risk_score":.9,"location_risk_score":.9,
       "previous_failed_transactions":4,"previous_fraud_history":1}
    r=investigate(t,{"fraud_probability":.95,"prediction":"FRAUD"})
    assert r["risk_level"]=="HIGH"
    assert r["decision"]=="BLOCK"
