import streamlit as st
import pandas as pd


# ==========================================================
# KPI Cards
# ==========================================================

def show_kpis(df):

    total_logs = len(df)

    threats = (df["Predicted Attack"] != "Normal").sum()

    critical = (df["Severity"] == "Critical").sum()

    avg_conf = round(df["Confidence"].mean(), 2)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📝 Total Logs",
        f"{total_logs:,}"
    )

    c2.metric(
        "🚨 Threats",
        f"{threats:,}"
    )

    c3.metric(
        "🔴 Critical Alerts",
        f"{critical:,}"
    )

    c4.metric(
        "🎯 Avg Confidence",
        f"{avg_conf}%"
    )


# ==========================================================
# Severity Badge
# ==========================================================

def severity_badge(level):

    if level == "Critical":
        st.error(f"🔴 {level}")

    elif level == "High":
        st.warning(f"🟠 {level}")

    elif level == "Medium":
        st.info(f"🔵 {level}")

    else:
        st.success(f"🟢 {level}")


# ==========================================================
# Recent Alerts
# ==========================================================

def recent_alerts(df):

    alerts = df[
        df["Predicted Attack"] != "Normal"
    ].copy()

    alerts = alerts.sort_values(
        "Confidence",
        ascending=False
    )

    cols = [
        "user_id",
        "Predicted Attack",
        "Severity",
        "Confidence"
    ]

    cols = [c for c in cols if c in alerts.columns]

    st.dataframe(
        alerts[cols].head(15),
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# Alert Explorer
# ==========================================================

def alert_explorer(df):

    alerts = df[
        df["Predicted Attack"] != "Normal"
    ].copy()

    alerts = alerts.reset_index(drop=True)

    alerts["Display"] = (
        alerts["user_id"]
        + "  |  "
        + alerts["Predicted Attack"]
        + "  |  "
        + alerts["Severity"]
    )

    selected = st.selectbox(
        "Select Alert",
        alerts["Display"]
    )

    row = alerts[
        alerts["Display"] == selected
    ].iloc[0]

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:

        st.subheader("Attack")
        st.write(row["Predicted Attack"])

        st.subheader("Confidence")
        st.write(f"{row['Confidence']} %")

    with c2:

        st.subheader("Severity")
        severity_badge(row["Severity"])

    st.markdown("---")

    st.subheader("📌 Reasons")

    for reason in str(row["Reasons"]).split("\n"):
        st.write(f"• {reason}")

    st.markdown("---")

    st.subheader("🛡 Recommended Actions")

    for action in str(row["Recommended Actions"]).split("\n"):
        st.write(f"✅ {action}")


# ==========================================================
# Footer
# ==========================================================

def footer():

    st.markdown("---")

    st.caption(
        "SentinelAI • Honeywell Hackathon MVP • AI Behavioural Threat Detection"
    )