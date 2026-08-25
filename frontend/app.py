import streamlit as st
from api_client import analyze_transaction

st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(0,180,255,.08), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(120,70,255,.08), transparent 30%),
        #070b14;
    color: #f1f5f9;
}

.main .block-container {
    max-width: 1450px;
    padding-top: 2rem;
}

.hero {
    padding: 28px 32px;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(15,23,42,.98), rgba(15,23,42,.82));
    border: 1px solid rgba(148,163,184,.16);
    box-shadow: 0 20px 60px rgba(0,0,0,.35);
    margin-bottom: 24px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
}

.hero-subtitle {
    color: #94a3b8;
    font-size: 16px;
    margin-top: 5px;
}

.status-pill {
    display: inline-block;
    margin-top: 14px;
    padding: 7px 14px;
    border-radius: 999px;
    background: rgba(34,197,94,.12);
    border: 1px solid rgba(34,197,94,.3);
    color: #4ade80;
    font-size: 13px;
    font-weight: 700;
}

.section-title {
    font-size: 22px;
    font-weight: 750;
    margin-top: 15px;
}

.section-description {
    color: #94a3b8;
    margin-bottom: 18px;
}

.metric-card {
    padding: 22px;
    border-radius: 18px;
    background: rgba(15,23,42,.82);
    border: 1px solid rgba(148,163,184,.13);
    min-height: 120px;
}

.metric-label {
    color: #94a3b8;
    font-size: 13px;
}

.metric-value {
    font-size: 28px;
    font-weight: 800;
    margin-top: 7px;
}

.metric-description {
    color: #64748b;
    font-size: 12px;
    margin-top: 5px;
}

.risk-card {
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 12px;
    background: rgba(15,23,42,.9);
    border: 1px solid rgba(148,163,184,.12);
}

.risk-card-title {
    font-size: 15px;
    font-weight: 700;
}

.risk-card-text {
    color: #94a3b8;
    font-size: 13px;
    line-height: 1.7;
}

.decision-box {
    text-align: center;
    padding: 28px;
    border-radius: 22px;
    margin: 20px 0;
    background: rgba(15,23,42,.9);
    border: 1px solid rgba(148,163,184,.15);
}

.decision-title {
    color: #94a3b8;
    font-size: 13px;
    letter-spacing: 2px;
}

.decision-value {
    font-size: 42px;
    font-weight: 900;
    margin-top: 8px;
}

.stButton > button {
    border-radius: 12px;
    font-weight: 750;
    min-height: 48px;
}

section[data-testid="stSidebar"] {
    background: #090e1a;
    border-right: 1px solid rgba(148,163,184,.12);
}

.footer {
    text-align: center;
    color: #475569;
    font-size: 12px;
    margin-top: 45px;
    padding-top: 20px;
    border-top: 1px solid rgba(148,163,184,.08);
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero">
    <div class="hero-title">🛡️ FraudGuard AI</div>
    <div class="hero-subtitle">
        Intelligent Transaction Fraud Detection & Investigation Platform
    </div>
    <div class="status-pill">● AI INVESTIGATION ENGINE ONLINE</div>
</div>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("## ⚙️ Investigation Center")
    st.caption("Configure transaction intelligence parameters.")

    st.info(
        "Combines machine-learning fraud probability "
        "with rule-based investigation."
    )

    st.markdown("---")

    st.markdown("### 📡 Detection Pipeline")

    st.markdown("""
    Transaction  
    ↓  
    ML Prediction  
    ↓  
    Risk Investigation  
    ↓  
    AI Explanation  
    ↓  
    Final Decision
    """)

    st.markdown("---")
    st.caption("FraudGuard AI • v1.0")


st.markdown(
    '<div class="section-title">💳 Transaction Investigation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Enter transaction and behavioral information to analyze fraud risk.'
    '</div>',
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


with col1:
    st.markdown("#### 💰 Transaction")

    amount = st.number_input(
        "Transaction Amount",
        min_value=1.0,
        value=2500.0,
        step=100.0
    )

    transaction_day = st.number_input(
    "Transaction Day",
    min_value=1,
    max_value=6,
    value=3
  )

    transaction_hour = st.slider(
        "Transaction Hour",
        min_value=0,
        max_value=23,
        value=14
    )

    customer_age = st.number_input(
        "Customer Age",
        min_value=18,
        max_value=100,
        value=30
    )

    account_age_days = st.number_input(
        "Account Age (Days)",
        min_value=1,
        value=500
    )


with col2:
    st.markdown("#### 📊 Behavioral Signals")

    customer_transaction_frequency = st.number_input(
        "Transaction Frequency",
        min_value=0.0,
        value=5.0,
        step=1.0
    )

    average_transaction_amount = st.number_input(
        "Average Transaction Amount",
        min_value=0.0,
        value=2000.0,
        step=100.0
    )

    recent_transaction_count = st.number_input(
        "Recent Transaction Count",
        min_value=0,
        value=3
    )

    previous_failed_transactions = st.number_input(
        "Previous Failed Transactions",
        min_value=0,
        value=0
    )

    previous_fraud_history = st.selectbox(
        "Previous Fraud History",
        [0, 1],
        format_func=lambda x: "No" if x == 0 else "Yes"
    )


with col3:
    st.markdown("#### 🌐 Security Signals")

    distance_from_usual_location = st.number_input(
        "Distance From Usual Location",
        min_value=0.0,
        value=20.0,
        step=10.0
    )

    device_risk_score = st.slider(
        "Device Risk Score",
        0.0,
        1.0,
        0.2,
        0.05
    )

    location_risk_score = st.slider(
        "Location Risk Score",
        0.0,
        1.0,
        0.2,
        0.05
    )

    merchant_category = st.selectbox(
        "Merchant Category",
        [
            "grocery",
            "electronics",
            "travel",
            "restaurant",
            "shopping",
            "fuel",
            "entertainment"
        ]
    )

    payment_method = st.selectbox(
        "Payment Method",
        [
            "upi",
            "card",
            "net_banking",
            "wallet"
        ]
    )


st.divider()

st.markdown(
    '<div class="section-title">📡 Real-Time Risk Signals</div>',
    unsafe_allow_html=True
)

r1, r2, r3, r4 = st.columns(4)

with r1:
    st.metric("Device Risk", f"{device_risk_score:.0%}")

with r2:
    st.metric("Location Risk", f"{location_risk_score:.0%}")

with r3:
    st.metric("Failed Transactions", previous_failed_transactions)

with r4:
    st.metric("Recent Activity", recent_transaction_count)


st.divider()

_, button_col, _ = st.columns([1, 2, 1])

with button_col:
    investigate = st.button(
        "🔍 INVESTIGATE TRANSACTION",
        type="primary",
        use_container_width=True
    )


if investigate:

    transaction = {
        "amount": amount,
        "transaction_day": transaction_day,
        "transaction_hour": transaction_hour,
        "customer_age": customer_age,
        "customer_transaction_frequency": customer_transaction_frequency,
        "average_transaction_amount": average_transaction_amount,
        "distance_from_usual_location": distance_from_usual_location,
        "device_risk_score": device_risk_score,
        "location_risk_score": location_risk_score,
        "previous_failed_transactions": previous_failed_transactions,
        "previous_fraud_history": previous_fraud_history,
        "recent_transaction_count": recent_transaction_count,
        "account_age_days": account_age_days,
        "merchant_category": merchant_category,
        "payment_method": payment_method
    }

    try:
        with st.spinner("🧠 Analyzing transaction..."):
            result = analyze_transaction(transaction)

        st.success("Investigation completed successfully.")

        fraud_probability = result.get("fraud_probability", 0)
        prediction = result.get("prediction", "UNKNOWN")
        risk_level = result.get("risk_level", "UNKNOWN")
        decision = result.get("decision", "UNKNOWN")
        confidence = result.get("confidence", 0)

        st.divider()

        st.markdown(
            '<div class="section-title">🎯 Investigation Verdict</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">FRAUD PROBABILITY</div>
                    <div class="metric-value">{fraud_probability:.2%}</div>
                    <div class="metric-description">ML model score</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">ML PREDICTION</div>
                    <div class="metric-value">{prediction}</div>
                    <div class="metric-description">Model classification</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">RISK LEVEL</div>
                    <div class="metric-value">{risk_level}</div>
                    <div class="metric-description">Risk classification</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with c4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">CONFIDENCE</div>
                    <div class="metric-value">{confidence:.2%}</div>
                    <div class="metric-description">Agent confidence</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            f"""
            <div class="decision-box">
                <div class="decision-title">FINAL TRANSACTION DECISION</div>
                <div class="decision-value">{decision}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader("📈 Fraud Risk Score")

        st.progress(
            min(max(float(fraud_probability), 0), 1)
        )

        if fraud_probability >= 0.75:
            st.error("🚨 HIGH RISK — Immediate attention required.")
        elif fraud_probability >= 0.35:
            st.warning("⚠️ MEDIUM RISK — Additional verification recommended.")
        else:
            st.success("✅ LOW RISK — Transaction appears legitimate.")

        left, right = st.columns(2)

        with left:
            st.markdown(
                '<div class="section-title">🔎 Risk Factors</div>',
                unsafe_allow_html=True
            )

            factors = result.get("top_risk_factors", [])

            if factors:
                for factor in factors:
                    st.markdown(
                        f"""
                        <div class="risk-card">
                            <div class="risk-card-title">⚠️ {factor}</div>
                            <div class="risk-card-text">
                                Identified during transaction investigation.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.success("No major risk factors detected.")

        with right:
            st.markdown(
                '<div class="section-title">📌 Recommended Action</div>',
                unsafe_allow_html=True
            )

            st.info(
                result.get(
                    "recommended_action",
                    "No recommendation available."
                )
            )

            st.markdown(
                '<div class="section-title">📝 Investigation Summary</div>',
                unsafe_allow_html=True
            )

            st.write(
                result.get(
                    "investigation_summary",
                    "No summary available."
                )
            )

        st.divider()

        st.markdown(
            '<div class="section-title">🤖 AI Investigation Explanation</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="risk-card">
                <div class="risk-card-text" style="font-size:15px;">
                    {result.get("explanation", "No explanation available.")}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander("📋 View Transaction Details"):
            st.json(transaction)

        with st.expander("🔧 View API Response"):
            st.json(result)

    except Exception as e:
        st.error(f"❌ Could not analyze transaction: {e}")


st.markdown(
    """
    <div class="footer">
        🛡️ FraudGuard AI • Machine Learning • AI Investigation Agent • FastAPI
    </div>
    """,
    unsafe_allow_html=True
)