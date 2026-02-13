import streamlit as st
import numpy as np
import pandas as pd
import joblib
import time
from datetime import datetime
import tensorflow as tf
from tensorflow.keras.models import load_model
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="Enterprise Zero-Day IDS",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================================
# CUSTOM ENTERPRISE UI STYLE
# ==========================================================
st.markdown("""
<style>
html, body, [class*="css"]  {
    background-color: #0e1117;
    color: white;
}
.main-title {
    font-size: 34px;
    font-weight: 700;
}
.sub-title {
    color: #9ca3af;
    margin-bottom: 20px;
}
.metric-card {
    background: linear-gradient(145deg, #1f2937, #111827);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.6);
}
.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD MODEL + SCALER + THRESHOLD
# ==========================================================
@st.cache_resource
def load_artifacts():
    model = load_model("models/autoencoder_zero_day.keras")
    scaler = joblib.load("models/scaler.pkl")
    threshold = np.load("models/threshold.npy")
    return model, scaler, threshold

model, scaler, threshold = load_artifacts()

# ==========================================================
# LOAD TEST DATASET (UNSEEN DATA)
# IMPORTANT: Must contain SAME 33 FEATURES as training
# If label column exists, name it 'Label'
# ==========================================================
@st.cache_data
def load_test_data():
    df = pd.read_csv("data/test_data.csv")
    return df

try:
    df_test = load_test_data()
except:
    st.error("Test dataset not found. Place it inside data/test_dataset.csv")
    st.stop()

# Separate features
if "Label" in df_test.columns:
    X_test = df_test.drop("Label", axis=1).values
    y_test = df_test["Label"].values
else:
    X_test = df_test.values
    y_test = None

# ==========================================================
# HEADER
# ==========================================================
st.markdown("<div class='main-title'>🛡️ Enterprise Zero-Day Intrusion Detection System</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Real-Time AI Powered Threat Monitoring (Dataset Replay Mode)</div>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================================
# SIDEBAR CONTROLS
# ==========================================================
st.sidebar.header("⚙️ Replay Control Panel")
start_button = st.sidebar.button("🚀 Start Traffic Replay")
speed = st.sidebar.slider("Replay Speed (ms per flow)", 50, 1000, 200)

# ==========================================================
# DASHBOARD PLACEHOLDERS
# ==========================================================
col1, col2, col3 = st.columns(3)
original_metric1 = col1.empty()
original_metric2 = col2.empty()
original_metric3 = col3.empty()

col4, col5, col6 = st.columns(3)
metric_placeholder1 = col4.empty()
metric_placeholder2 = col5.empty()
metric_placeholder3 = col6.empty()

chart_placeholder = st.empty()
log_placeholder = st.empty()

# ==========================================================
# MAIN REPLAY LOOP
# ==========================================================
if start_button:

    scaled_data = scaler.transform(X_test)
    reconstructed = model.predict(scaled_data, verbose=0)
    errors_all = np.mean(np.square(scaled_data - reconstructed), axis=1)

    # ---------------- Original METRICS ----------------
    original_metric1.metric('Original Total Flows', load_test_data().shape[0])
    original_metric2.metric('Original Normal Traffic', load_test_data()['Label'].value_counts()[0])
    original_metric3.metric('Original Total Anomalies', load_test_data()['Label'].value_counts()[1])

    total_flows = 0
    anomaly_count = 0
    normal_count = 0
    error_history = []
    log_data = []

    for i in range(len(errors_all)):

        error = errors_all[i]
        error_history.append(error)
        total_flows += 1

        if error > threshold:
            anomaly_count += 1
            status = "🔴 Anomaly"
            log_data.append({
                "Timestamp": datetime.now(),
                "Flow Index": i,
                "Anomaly Score": float(error),
                "Status": "Blocked"
            })
        else:
            normal_count += 1
            status = "🟢 Normal"

        # ---------------- Predicted METRICS ----------------
        metric_placeholder1.metric("Total Flows Analyzed", total_flows)
        metric_placeholder2.metric("Predicted Normal Traffic", normal_count)
        metric_placeholder3.metric("Predicted Anomalies", anomaly_count)

        # ---------------- LIVE GRAPH ----------------
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=error_history, mode='lines', name='Anomaly Score'))
        fig.add_hline(y=float(threshold), line_dash="dash", annotation_text="Threshold")
        fig.update_layout(
            template="plotly_dark",
            height=400,
            title="Live Reconstruction Error Monitoring"
        )
        chart_placeholder.plotly_chart(fig, use_container_width=True)

        # ---------------- LOG TABLE ----------------
        if len(log_data) > 0:
            df_log = pd.DataFrame(log_data)
            log_placeholder.dataframe(df_log.tail(10), use_container_width=True)

        time.sleep(speed / 1000)

else:
    st.info("Click 'Start Traffic Replay' to simulate real-time network monitoring using unseen test data.")

# ==========================================================
# FOOTER
# ==========================================================
st.markdown("---")
st.caption("© 2026 Enterprise Zero-Day IDS | Real-Time Dataset Replay Mode")