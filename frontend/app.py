import streamlit as st
from api_client import analyze_transaction


st.set_page_config(page_title="AI Fraud Investigator",page_icon="🛡️",layout="wide")
st.title("🛡️ AI Fraud Detection & Investigation Agent")
st.caption("Simple ML model + investigation agent + FastAPI")

c1,c2,c3 = st.columns(3)
with c1:
    amount=st.number_input("Amount",min_value=1.0,value=2500.0)
    hour=st.number_input("Transaction Hour",0,23,14)
    distance=st.number_input("Distance From Usual Location",min_value=0.0,value=20.0)
    merchant=st.selectbox("Merchant Category",["grocery","electronics","travel","fashion","gaming"])
with c2:
    device=st.slider("Device Risk",0.0,1.0,0.2)
    location=st.slider("Location Risk",0.0,1.0,0.2)
    failed=st.number_input("Previous Failed Transactions",min_value=0,value=0)
    recent=st.number_input("Recent Transaction Count",min_value=0,value=3)
with c3:
    previous=st.selectbox("Previous Fraud History",[0,1])
    age=st.number_input("Account Age (days)",min_value=1,value=500)
    payment=st.selectbox("Payment Method",["card","upi","netbanking"])

if st.button("🔍 Investigate Transaction",type="primary"):
    data={"amount":amount,"transaction_hour":hour,
          "distance_from_usual_location":distance,
          "device_risk_score":device,"location_risk_score":location,
          "previous_failed_transactions":failed,
          "previous_fraud_history":previous,
          "recent_transaction_count":recent,
          "account_age_days":age,"merchant_category":merchant,
          "payment_method":payment}
    try:
        r=analyze_transaction(data)
        a,b,c=st.columns(3)
        a.metric("Fraud Probability",f"{r['fraud_probability']:.1%}")
        b.metric("Risk Level",r["risk_level"])
        c.metric("Decision",r["decision"])
        st.subheader("AI Investigation")
        st.write(r["investigation_summary"])
        st.subheader("Risk Factors")
        if r["top_risk_factors"]:
            for x in r["top_risk_factors"]: st.warning(x)
        else: st.success("No major risk factors detected.")
        st.subheader("Recommended Action")
        st.info(r["recommended_action"])
        st.subheader("Explanation")
        st.write(r["explanation"])
    except Exception as e:
        st.error(f"Could not analyze transaction: {e}")
