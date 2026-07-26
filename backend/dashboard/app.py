from pathlib import Path

import pandas as pd
import streamlit as st

from charts import (
    threat_distribution,
    country_distribution,
    department_distribution,
    login_hour_distribution,
    confidence_distribution,
    severity_distribution,
    security_score
)

from utils import (
    show_kpis,
    recent_alerts,
    alert_explorer,
    footer
)

# =====================================================
# Page Config
# =====================================================

st.set_page_config(
    page_title="SentinelAI",
    page_icon="🛡️",
    layout="wide"
)

# =====================================================
# Load Dataset
# =====================================================

CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent

DATA_PATH = (
    BACKEND_DIR
    / "datasets"
    / "predictions_with_explanations.csv"
)

df = pd.read_csv(DATA_PATH)

# =====================================================
# Sidebar
# =====================================================

LOGO_PATH = CURRENT_DIR / "assets" / "logo.png"

st.sidebar.image(LOGO_PATH, width=90)

st.sidebar.title("SentinelAI")

attack = st.sidebar.selectbox(
    "Attack Type",
    ["All"] + sorted(df["Predicted Attack"].unique())
)

severity = st.sidebar.selectbox(
    "Severity",
    ["All"] + sorted(df["Severity"].unique())
)

filtered = df.copy()

if attack != "All":
    filtered = filtered[
        filtered["Predicted Attack"] == attack
    ]

if severity != "All":
    filtered = filtered[
        filtered["Severity"] == severity
    ]

# =====================================================
# Title
# =====================================================

st.title("🛡️ SentinelAI")
st.caption(
    "Enterprise AI-Powered Behavioural Threat Detection Platform"
)

st.divider()

# =====================================================
# KPIs
# =====================================================

show_kpis(filtered)

st.divider()

# =====================================================
# Charts Row 1
# =====================================================

c1, c2 = st.columns(2)

with c1:
    st.plotly_chart(
        threat_distribution(filtered),
        use_container_width=True
    )

with c2:
    st.plotly_chart(
        country_distribution(filtered),
        use_container_width=True
    )

# =====================================================
# Charts Row 2
# =====================================================

c3, c4 = st.columns(2)

with c3:
    st.plotly_chart(
        department_distribution(filtered),
        use_container_width=True
    )

with c4:
    st.plotly_chart(
        login_hour_distribution(filtered),
        use_container_width=True
    )

# =====================================================
# Charts Row 3
# =====================================================

c5, c6 = st.columns(2)

with c5:
    st.plotly_chart(
        severity_distribution(filtered),
        use_container_width=True
    )

with c6:
    st.plotly_chart(
        security_score(filtered),
        use_container_width=True
    )

st.divider()

# =====================================================
# Recent Alerts
# =====================================================

st.subheader("🚨 Recent High-Risk Alerts")

recent_alerts(filtered)

st.divider()

# =====================================================
# Alert Explorer
# =====================================================

st.subheader("🔍 Alert Explorer")

alert_explorer(filtered)

footer()