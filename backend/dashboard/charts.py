import plotly.express as px
import plotly.graph_objects as go


# =========================================================
# Threat Distribution
# =========================================================

def threat_distribution(df):

    attack_df = df[df["Predicted Attack"] != "Normal"]

    data = (
        attack_df["Predicted Attack"]
        .value_counts()
        .reset_index()
    )

    data.columns = ["Attack", "Count"]

    fig = px.bar(
        data,
        x="Attack",
        y="Count",
        color="Attack",
        title="Threat Distribution",
        text="Count"
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title="Attack Type",
        yaxis_title="Incidents",
        height=420
    )

    return fig


# =========================================================
# Threats by Country
# =========================================================

def country_distribution(df):

    attack_df = df[df["Predicted Attack"] != "Normal"]

    data = (
        attack_df["country"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    data.columns = ["Country", "Count"]

    fig = px.bar(
        data,
        x="Country",
        y="Count",
        color="Country",
        title="Top Threat Countries",
        text="Count"
    )

    fig.update_layout(
        showlegend=False,
        height=420
    )

    return fig


# =========================================================
# Threats by Department
# =========================================================

def department_distribution(df):

    attack_df = df[df["Predicted Attack"] != "Normal"]

    data = (
        attack_df["department"]
        .value_counts()
        .reset_index()
    )

    data.columns = ["Department", "Count"]

    fig = px.pie(
        data,
        names="Department",
        values="Count",
        hole=0.55,
        title="Threats by Department"
    )

    fig.update_layout(
        height=420
    )

    return fig


# =========================================================
# Login Hour Distribution
# =========================================================

def login_hour_distribution(df):

    attack_df = df[df["Predicted Attack"] != "Normal"]

    data = (
        attack_df.groupby("login_hour")
        .size()
        .reset_index(name="Count")
        .sort_values("login_hour")
    )

    fig = px.line(
        data,
        x="login_hour",
        y="Count",
        markers=True,
        title="Threats by Login Hour"
    )

    fig.update_layout(
        xaxis_title="Hour",
        yaxis_title="Threat Count",
        height=420
    )

    return fig


# =========================================================
# Confidence Histogram
# =========================================================

def confidence_distribution(df):

    fig = px.histogram(
        df,
        x="Confidence",
        nbins=25,
        title="Prediction Confidence"
    )

    fig.update_layout(
        height=420
    )

    return fig


# =========================================================
# Severity Donut
# =========================================================

def severity_distribution(df):

    data = (
        df["Severity"]
        .value_counts()
        .reset_index()
    )

    data.columns = ["Severity", "Count"]

    fig = px.pie(
        data,
        names="Severity",
        values="Count",
        hole=0.60,
        title="Threat Severity"
    )

    fig.update_layout(
        height=420
    )

    return fig


# =========================================================
# Gauge Chart
# =========================================================

def security_score(df):

    threats = (df["Predicted Attack"] != "Normal").sum()

    total = len(df)

    score = max(
        0,
        100 - (threats / total) * 100
    )

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={"text": "Security Score"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"thickness": 0.3},
            "steps": [
                {"range": [0, 40]},
                {"range": [40, 70]},
                {"range": [70, 100]}
            ]
        }
    ))

    fig.update_layout(
        height=350
    )

    return fig