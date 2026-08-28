import json
from pathlib import Path

import plotly.graph_objects as go
import streamlit as st

from api_client import analyze_transaction


st.set_page_config(
    page_title="FraudGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown(
    """
    <style>

    .stApp {
        background: #f5f7fb;
        color: #101828;
    }

    [data-testid="stHeader"] {
        background: #f5f7fb;
    }

    .block-container {
        max-width: 1550px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        background: #081525;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    .brand {
        font-size: 28px;
        font-weight: 900;
        color: #ffffff !important;
    }

    .brand-blue {
        color: #3b9cff !important;
    }

    .sidebar-subtitle {
        color: #3b9cff !important;
        font-size: 15px;
        font-weight: 800;
        margin-top: 5px;
    }

    .sidebar-description {
        color: #d0d5dd !important;
        font-size: 13px;
        line-height: 1.7;
        margin-top: 15px;
    }

    .sidebar-heading {
        color: #ffffff !important;
        font-size: 17px;
        font-weight: 850;
        margin-top: 22px;
        margin-bottom: 12px;
    }

    .pipeline-box {
        background: #122238;
        border: 1px solid #243852;
        border-radius: 11px;
        padding: 10px 12px;
        margin-bottom: 8px;
    }

    .pipeline-title {
        color: #ffffff !important;
        font-size: 13px;
        font-weight: 800;
    }

    .pipeline-description {
        color: #aebaca !important;
        font-size: 10px;
        margin-top: 3px;
    }

    .defense-box {
        background: #09251a;
        border: 1px solid #168747;
        border-radius: 12px;
        padding: 14px;
        margin-top: 22px;
    }

    .defense-title {
        color: #4ade80 !important;
        font-size: 13px;
        font-weight: 900;
    }

    .defense-text {
        color: #d1fae5 !important;
        font-size: 11px;
        line-height: 1.5;
        margin-top: 5px;
    }

    .main-title {
        color: #101828 !important;
        font-size: 43px;
        font-weight: 900;
        line-height: 1.1;
        margin-bottom: 4px;
    }

    .main-title-blue {
        color: #1677e8 !important;
    }

    .subtitle {
        color: #475467 !important;
        font-size: 16px;
        margin-bottom: 22px;
    }

    .section-title {
        color: #101828 !important;
        font-size: 23px;
        font-weight: 900;
        margin-top: 7px;
        margin-bottom: 4px;
    }

    .section-description {
        color: #475467 !important;
        font-size: 13px;
        margin-bottom: 15px;
    }

    .metric-card {
        background: #ffffff;
        border: 1px solid #d9e0e8;
        border-radius: 13px;
        padding: 15px 8px;
        text-align: center;
        min-height: 105px;
        box-shadow: 0 2px 7px rgba(16, 24, 40, 0.05);
    }

    .metric-label {
        color: #344054 !important;
        font-size: 12px;
        font-weight: 800;
    }

    .metric-value {
        color: #101828 !important;
        font-size: 25px;
        font-weight: 900;
        margin-top: 7px;
    }

    .blue {
        color: #1677e8 !important;
    }

    .purple {
        color: #6941c6 !important;
    }

    .green {
        color: #087443 !important;
    }

    .orange {
        color: #b54708 !important;
    }

    .red {
        color: #b42318 !important;
    }

    .dashboard-card {
        background: #ffffff;
        border: 1px solid #d9e0e8;
        border-radius: 15px;
        padding: 18px;
        box-shadow: 0 2px 8px rgba(16, 24, 40, 0.05);
    }

    .form-heading {
        color: #101828 !important;
        font-size: 17px;
        font-weight: 900;
        margin-top: 9px;
        margin-bottom: 12px;
    }

    label {
        color: #101828 !important;
        font-weight: 750 !important;
    }

    .stNumberInput input {
        color: #101828 !important;
        background: #ffffff !important;
        border: 1px solid #b8c2ce !important;
        font-weight: 600 !important;
    }

    .stTextInput input {
        color: #101828 !important;
        background: #ffffff !important;
        border: 1px solid #b8c2ce !important;
    }

    div[data-baseweb="select"] > div {
        background: #ffffff !important;
        border-color: #b8c2ce !important;
    }

    div[data-baseweb="select"] * {
        color: #101828 !important;
        font-weight: 600 !important;
    }

    .stSlider label {
        color: #101828 !important;
    }

    .investigate-box {
        background: #edf6ff;
        border: 2px solid #7db8ff;
        border-radius: 12px;
        padding: 12px;
        margin-top: 12px;
        text-align: center;
    }

    .investigate-text {
        color: #0b5cab !important;
        font-size: 13px;
        font-weight: 850;
        margin-bottom: 8px;
    }

    div[data-testid="stFormSubmitButton"] button {
        width: 100%;
        min-height: 58px;
        background: #1769e8 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 11px !important;
        font-size: 17px !important;
        font-weight: 900 !important;
        box-shadow: 0 5px 13px rgba(23, 105, 232, 0.25);
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        background: #075fcf !important;
        color: #ffffff !important;
    }

    .decision-block {
        background: #fff0ef;
        border: 1px solid #f1b8b4;
        border-left: 6px solid #d92d20;
        border-radius: 13px;
        padding: 19px;
    }

    .decision-review {
        background: #fff8e7;
        border: 1px solid #f0d19a;
        border-left: 6px solid #f79009;
        border-radius: 13px;
        padding: 19px;
    }

    .decision-approve {
        background: #eafaf1;
        border: 1px solid #a8dfbf;
        border-left: 6px solid #12b76a;
        border-radius: 13px;
        padding: 19px;
    }

    .decision-title {
        font-size: 26px;
        font-weight: 900;
    }

    .decision-block .decision-title {
        color: #b42318 !important;
    }

    .decision-review .decision-title {
        color: #b54708 !important;
    }

    .decision-approve .decision-title {
        color: #087443 !important;
    }

    .decision-details {
        color: #344054 !important;
        font-size: 13px;
        line-height: 1.8;
        margin-top: 5px;
    }

    .decision-details strong {
        color: #101828 !important;
    }

    .risk-factor {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-left: 4px solid #f97316;
        border-radius: 9px;
        padding: 10px 13px;
        margin-bottom: 7px;
        color: #7c2d12 !important;
        font-size: 13px;
        font-weight: 750;
    }

    .safe-factor {
        background: #ecfdf3;
        border: 1px solid #bbf7d0;
        border-left: 4px solid #22c55e;
        border-radius: 9px;
        padding: 12px;
        color: #166534 !important;
        font-weight: 750;
    }

    .info-card {
        background: #ffffff;
        border: 1px solid #d9e0e8;
        border-radius: 11px;
        padding: 15px;
        min-height: 105px;
        box-shadow: 0 2px 7px rgba(16, 24, 40, 0.04);
    }

    .info-title {
        color: #101828 !important;
        font-size: 15px;
        font-weight: 900;
        margin-bottom: 6px;
    }

    .info-text {
        color: #344054 !important;
        font-size: 13px;
        line-height: 1.65;
    }

    [data-testid="stMetricLabel"] {
        color: #344054 !important;
        font-weight: 750 !important;
    }

    [data-testid="stMetricValue"] {
        color: #101828 !important;
        font-weight: 900 !important;
    }

    .stCaption {
        color: #667085 !important;
    }

    .stExpander {
        background: #ffffff !important;
        border: 1px solid #d9e0e8 !important;
        border-radius: 10px !important;
    }

    .stExpander summary {
        color: #101828 !important;
        font-weight: 800 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


def load_evaluation():

    path = Path("models/evaluation.json")

    if not path.exists():
        return {}

    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


def get_metric(data, keys, default=0):

    for key in keys:

        if key in data:

            try:
                return float(data[key])
            except Exception:
                pass

    return default


evaluation = load_evaluation()

metrics = evaluation.get(
    "held_out_test_metrics",
    evaluation.get("metrics", {})
)

threshold = float(
    evaluation.get(
        "decision_threshold",
        0.4
    )
)

roc_auc = get_metric(
    metrics,
    ["roc_auc", "ROC-AUC"]
)

pr_auc = get_metric(
    metrics,
    ["pr_auc", "PR-AUC"]
)

precision = get_metric(
    metrics,
    ["precision", "Precision"]
)

recall = get_metric(
    metrics,
    ["recall", "Recall"]
)

f1 = get_metric(
    metrics,
    ["f1_score", "f1", "F1 Score"]
)


with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            🛡️ FraudGuard <span class="brand-blue">AI</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">AI Risk Manager</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="sidebar-description">
            Detect suspicious transactions, investigate risk signals,
            and recommend an appropriate defensive action.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown(
        '<div class="sidebar-heading">SYSTEM PIPELINE</div>',
        unsafe_allow_html=True
    )

    pipeline = [
        ("💳", "Transaction", "Transaction information"),
        ("🧠", "ML Detection", "Fraud probability"),
        ("📊", "Risk Analysis", "Risk signal evaluation"),
        ("🔎", "Investigation", "Rule-based investigation"),
        ("🛡️", "Decision", "Approve / Review / Block"),
        ("💡", "Explanation", "Recommended action")
    ]

    for icon, title, description in pipeline:

        st.markdown(
            f"""
            <div class="pipeline-box">
                <div class="pipeline-title">
                    {icon} {title}
                </div>
                <div class="pipeline-description">
                    {description}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
        <div class="defense-box">
            <div class="defense-title">
                🛡️ DEFENSE-ONLY SYSTEM
            </div>
            <div class="defense-text">
                Built to detect, investigate, and reduce
                transaction fraud risk.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    """
    <div class="main-title">
        🛡️ FraudGuard <span class="main-title-blue">AI</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        AI-powered transaction fraud detection and investigation platform
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    '<div class="section-title">📊 Model Performance Overview</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-description">
        Model performance measured on a held-out 20% test set.
    </div>
    """,
    unsafe_allow_html=True
)


m1, m2, m3, m4, m5, m6 = st.columns(6)

metric_items = [
    (m1, "ROC-AUC", f"{roc_auc:.4f}", "blue"),
    (m2, "PR-AUC", f"{pr_auc:.4f}", "purple"),
    (m3, "Precision", f"{precision:.2%}", "green"),
    (m4, "Recall", f"{recall:.2%}", "orange"),
    (m5, "F1 Score", f"{f1:.2%}", "red"),
    (m6, "Decision Threshold", f"{threshold:.0%}", "blue")
]

for column, label, value, color_class in metric_items:

    with column:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value {color_class}">
                    {value}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown("")


performance_fig = go.Figure()

performance_fig.add_trace(
    go.Bar(
        x=[
            "ROC-AUC",
            "PR-AUC",
            "Precision",
            "Recall",
            "F1 Score"
        ],
        y=[
            roc_auc,
            pr_auc,
            precision,
            recall,
            f1
        ],
        text=[
            f"{roc_auc:.2f}",
            f"{pr_auc:.2f}",
            f"{precision:.2f}",
            f"{recall:.2f}",
            f"{f1:.2f}"
        ],
        textposition="outside",
        textfont=dict(
            color="#101828",
            size=14
        ),
        marker=dict(
            color="#72b8ed"
        )
    )
)

performance_fig.update_layout(
    title=dict(
        text="Model Performance Chart",
        font=dict(
            color="#101828",
            size=19
        ),
        x=0.02
    ),
    xaxis=dict(
        title=dict(
            text="Metric",
            font=dict(
                color="#101828",
                size=14
            )
        ),
        tickfont=dict(
            color="#101828",
            size=13
        ),
        showline=True,
        linecolor="#101828"
    ),
    yaxis=dict(
        title=dict(
            text="Score",
            font=dict(
                color="#101828",
                size=14
            )
        ),
        tickfont=dict(
            color="#101828",
            size=13
        ),
        range=[0, 1],
        showgrid=True,
        gridcolor="#d0d5dd",
        showline=True,
        linecolor="#101828"
    ),
    height=360,
    margin=dict(
        l=60,
        r=35,
        t=70,
        b=60
    ),
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    font=dict(
        color="#101828"
    )
)

st.plotly_chart(
    performance_fig,
    use_container_width=True
)


st.divider()


st.markdown(
    '<div class="section-title">🔎 Transaction Investigation</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-description">
        Enter transaction, customer, behavioral, and security information.
    </div>
    """,
    unsafe_allow_html=True
)


with st.form("transaction_form"):

    st.markdown(
        '<div class="form-heading">💳 Transaction Details</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        amount = st.number_input(
            "Transaction Amount (₹)",
            min_value=1.0,
            value=2500.0,
            step=100.0
        )

    with c2:

        transaction_day = st.number_input(
            "Transaction Day",
            min_value=0,
            max_value=6,
            value=2,
            step=1,
            help="0 = Monday, 6 = Sunday"
        )

    with c3:

        transaction_hour = st.number_input(
            "Transaction Hour",
            min_value=0,
            max_value=23,
            value=14,
            step=1
        )


    c1, c2 = st.columns(2)

    with c1:

        merchant_category = st.selectbox(
            "Merchant Category",
            [
                "grocery",
                "electronics",
                "clothing",
                "travel",
                "food",
                "entertainment",
                "healthcare",
                "other"
            ]
        )

    with c2:

        payment_method = st.selectbox(
            "Payment Method",
            [
                "card",
                "upi",
                "bank_transfer",
                "wallet"
            ]
        )


    st.markdown(
        '<div class="form-heading">👤 Customer Profile</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        customer_age = st.number_input(
            "Customer Age",
            min_value=18,
            max_value=100,
            value=30,
            step=1
        )

    with c2:

        account_age_days = st.number_input(
            "Account Age (days)",
            min_value=1,
            value=500,
            step=10
        )

    with c3:

        customer_transaction_frequency = st.number_input(
            "Customer Transaction Frequency",
            min_value=0,
            value=5,
            step=1
        )


    average_transaction_amount = st.number_input(
        "Average Transaction Amount (₹)",
        min_value=0.0,
        value=2000.0,
        step=100.0
    )


    st.markdown(
        '<div class="form-heading">📈 Behavioral Signals</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        recent_transaction_count = st.number_input(
            "Recent Transaction Count",
            min_value=0,
            value=3,
            step=1
        )

    with c2:

        previous_failed_transactions = st.number_input(
            "Previous Failed Transactions",
            min_value=0,
            value=0,
            step=1
        )

    with c3:

        previous_fraud_history = st.selectbox(
            "Previous Fraud History",
            ["No", "Yes"]
        )


    st.markdown(
        '<div class="form-heading">🔐 Security Signals</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        device_risk_score = st.slider(
            "Device Risk Score",
            min_value=0.0,
            max_value=1.0,
            value=0.2,
            step=0.01
        )

    with c2:

        location_risk_score = st.slider(
            "Location Risk Score",
            min_value=0.0,
            max_value=1.0,
            value=0.2,
            step=0.01
        )

    with c3:

        distance_from_usual_location = st.number_input(
            "Distance From Usual Location (km)",
            min_value=0.0,
            value=20.0,
            step=10.0
        )


    st.markdown(
        """
        <div class="investigate-box">
            <div class="investigate-text">
                Ready to analyze this transaction?
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    submitted = st.form_submit_button(
        "🔍  INVESTIGATE TRANSACTION"
    )


if submitted:

    transaction = {
        "amount": float(amount),
        "transaction_day": int(transaction_day),
        "transaction_hour": int(transaction_hour),
        "customer_age": int(customer_age),
        "customer_transaction_frequency": int(
            customer_transaction_frequency
        ),
        "average_transaction_amount": float(
            average_transaction_amount
        ),
        "distance_from_usual_location": float(
            distance_from_usual_location
        ),
        "device_risk_score": float(
            device_risk_score
        ),
        "location_risk_score": float(
            location_risk_score
        ),
        "previous_failed_transactions": int(
            previous_failed_transactions
        ),
        "previous_fraud_history": (
            1
            if previous_fraud_history == "Yes"
            else 0
        ),
        "recent_transaction_count": int(
            recent_transaction_count
        ),
        "account_age_days": int(
            account_age_days
        ),
        "merchant_category": merchant_category,
        "payment_method": payment_method
    }

    with st.spinner(
        "🤖 Running ML fraud detection and investigation..."
    ):

        try:

            result = analyze_transaction(
                transaction
            )

            st.session_state["result"] = result

        except Exception as error:

            st.error(
                f"❌ Could not analyze transaction: {error}"
            )


if "result" in st.session_state:

    result = st.session_state["result"]

    probability = float(
        result.get(
            "fraud_probability",
            0
        )
    )

    prediction = result.get(
        "prediction",
        "UNKNOWN"
    )

    risk_level = result.get(
        "risk_level",
        "UNKNOWN"
    )

    decision = result.get(
        "decision",
        "UNKNOWN"
    )

    decision_threshold = float(
        result.get(
            "decision_threshold",
            threshold
        )
    )

    risk_factors = result.get(
        "top_risk_factors",
        []
    )

    recommended_action = result.get(
        "recommended_action",
        "No recommendation available."
    )

    investigation_summary = result.get(
        "investigation_summary",
        "No investigation summary available."
    )

    explanation = result.get(
        "explanation",
        "No explanation available."
    )


    st.divider()


    st.markdown(
        '<div class="section-title">🎯 Investigation Result</div>',
        unsafe_allow_html=True
    )


    if decision == "BLOCK":

        decision_class = "decision-block"
        decision_icon = "🚨"

    elif decision == "REVIEW":

        decision_class = "decision-review"
        decision_icon = "⚠️"

    else:

        decision_class = "decision-approve"
        decision_icon = "✅"


    st.markdown(
        f"""
        <div class="{decision_class}">
            <div class="decision-title">
                {decision_icon} {risk_level} RISK — {decision}
            </div>

            <div class="decision-details">
                <strong>Model Prediction:</strong> {prediction}<br>
                <strong>Fraud Probability:</strong> {probability:.2%}<br>
                <strong>Decision Threshold:</strong> {decision_threshold:.0%}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("")


    r1, r2, r3, r4 = st.columns(4)

    with r1:

        st.metric(
            "Fraud Probability",
            f"{probability:.2%}"
        )

    with r2:

        st.metric(
            "Risk Level",
            risk_level
        )

    with r3:

        st.metric(
            "Decision",
            decision
        )

    with r4:

        st.metric(
            "Threshold",
            f"{decision_threshold:.0%}"
        )


    st.markdown(
        '<div class="section-title">📈 Fraud Probability</div>',
        unsafe_allow_html=True
    )


    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probability * 100,
            number={
                "suffix": "%",
                "font": {
                    "size": 38,
                    "color": "#101828"
                }
            },
            title={
                "text": "Probability of Fraud",
                "font": {
                    "size": 17,
                    "color": "#101828"
                }
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "ticksuffix": "%",
                    "tickfont": {
                        "color": "#101828",
                        "size": 11
                    }
                },
                "bar": {
                    "color": "#1677e8",
                    "thickness": 0.28
                },
                "steps": [
                    {
                        "range": [0, 35],
                        "color": "#b7ebc9"
                    },
                    {
                        "range": [35, 70],
                        "color": "#f7dfaa"
                    },
                    {
                        "range": [70, 100],
                        "color": "#f2b8b4"
                    }
                ],
                "threshold": {
                    "line": {
                        "color": "#101828",
                        "width": 4
                    },
                    "thickness": 0.8,
                    "value": decision_threshold * 100
                }
            }
        )
    )

    gauge.update_layout(
        height=310,
        margin=dict(
            l=35,
            r=35,
            t=65,
            b=15
        ),
        paper_bgcolor="#ffffff",
        font={
            "color": "#101828"
        }
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )


    st.markdown(
        '<div class="section-title">📊 Risk Signal Analysis</div>',
        unsafe_allow_html=True
    )


    risk_data = {
        "Signal": [
            "Device Risk",
            "Location Risk",
            "Location Deviation",
            "Failed Transactions",
            "Previous Fraud",
            "Transaction Amount",
            "Transaction Frequency"
        ],
        "Score": [
            device_risk_score,
            location_risk_score,
            min(
                distance_from_usual_location / 500,
                1
            ),
            min(
                previous_failed_transactions / 5,
                1
            ),
            previous_fraud_history,
            min(
                amount / 50000,
                1
            ),
            min(
                customer_transaction_frequency / 20,
                1
            )
        ]
    }


    risk_fig = go.Figure()

    risk_fig.add_trace(
        go.Bar(
            x=risk_data["Score"],
            y=risk_data["Signal"],
            orientation="h",
            text=[
                str(value)
                for value in risk_data["Score"]
            ],
            textposition="outside",
            textfont=dict(
                color="#101828",
                size=12
            ),
            marker=dict(
                color="#72b8ed"
            )
        )
    )

    risk_fig.update_layout(
        title=dict(
            text="Transaction Risk Signals",
            font=dict(
                color="#101828",
                size=18
            ),
            x=0.02
        ),
        xaxis=dict(
            range=[0, 1.08],
            title=dict(
                text="Normalized Risk Level",
                font=dict(
                    color="#101828"
                )
            ),
            tickfont=dict(
                color="#101828"
            ),
            tickformat=".0%",
            gridcolor="#d0d5dd"
        ),
        yaxis=dict(
            title="",
            tickfont=dict(
                color="#101828",
                size=12
            )
        ),
        height=390,
        margin=dict(
            l=30,
            r=50,
            t=65,
            b=55
        ),
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font=dict(
            color="#101828"
        )
    )

    st.plotly_chart(
        risk_fig,
        use_container_width=True
    )


    left, right = st.columns(
        2,
        gap="large"
    )


    with left:

        st.markdown(
            '<div class="section-title">⚠️ Key Risk Factors</div>',
            unsafe_allow_html=True
        )

        if risk_factors:

            for factor in risk_factors:

                st.markdown(
                    f"""
                    <div class="risk-factor">
                        ⚠️ {factor}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.markdown(
                """
                <div class="safe-factor">
                    ✅ No major rule-based risk indicators were identified.
                </div>
                """,
                unsafe_allow_html=True
            )


    with right:

        st.markdown(
            '<div class="section-title">🤖 AI Investigation Summary</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-title">
                    Risk Assessment
                </div>

                <div class="info-text">
                    {investigation_summary}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("")


    left, right = st.columns(
        2,
        gap="large"
    )


    with left:

        st.markdown(
            '<div class="section-title">💡 Recommended Action</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-title">
                    {decision_icon} {decision}
                </div>

                <div class="info-text">
                    {recommended_action}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with right:

        st.markdown(
            '<div class="section-title">📝 AI Explanation</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-title">
                    Investigation Reasoning
                </div>

                <div class="info-text">
                    {explanation}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        '<div class="section-title">💰 Business Cost Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="section-description">
            Cost-sensitive evaluation of false positives and false negatives.
        </div>
        """,
        unsafe_allow_html=True
    )


    business_cost = evaluation.get(
        "business_cost",
        {}
    )

    false_positive_cost = business_cost.get(
        "false_positive_cost_per_case",
        0
    )

    false_negative_cost = business_cost.get(
        "false_negative_cost_per_case",
        0
    )

    total_estimated_cost = business_cost.get(
        "total_estimated_cost",
        0
    )


    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            label="FALSE POSITIVE COST",
            value=f"₹{false_positive_cost:,}"
        )

    with c2:

        st.metric(
            label="FALSE NEGATIVE COST",
            value=f"₹{false_negative_cost:,}"
        )

    with c3:

        st.metric(
            label="ESTIMATED TEST COST",
            value=f"₹{total_estimated_cost:,}"
        )


    if total_estimated_cost:

        cost_fig = go.Figure()

        cost_fig.add_trace(
            go.Bar(
                x=[
                    "False Positive",
                    "False Negative",
                    "Estimated Total"
                ],
                y=[
                    false_positive_cost,
                    false_negative_cost,
                    total_estimated_cost
                ],
                text=[
                    f"₹{false_positive_cost:,}",
                    f"₹{false_negative_cost:,}",
                    f"₹{total_estimated_cost:,}"
                ],
                textposition="outside",
                textfont=dict(
                    color="#101828",
                    size=13
                ),
                marker=dict(
                    color="#72b8ed"
                )
            )
        )

        cost_fig.update_layout(
            title=dict(
                text="Estimated Business Cost",
                font=dict(
                    color="#101828",
                    size=18
                ),
                x=0.02
            ),
            xaxis=dict(
                title="",
                tickfont=dict(
                    color="#101828",
                    size=12
                )
            ),
            yaxis=dict(
                title=dict(
                    text="Cost (₹)",
                    font=dict(
                        color="#101828",
                        size=13
                    )
                ),
                tickfont=dict(
                    color="#101828",
                    size=12
                ),
                gridcolor="#d0d5dd"
            ),
            height=350,
            margin=dict(
                l=55,
                r=45,
                t=65,
                b=55
            ),
            paper_bgcolor="#ffffff",
            plot_bgcolor="#ffffff",
            font=dict(
                color="#101828"
            )
        )

        st.plotly_chart(
            cost_fig,
            use_container_width=True
        )


    st.caption(
        "Business-cost figures are demonstration assumptions used to evaluate false-positive and false-negative trade-offs."
    )


    with st.expander("🔎 View Raw API Response"):

        st.json(result)