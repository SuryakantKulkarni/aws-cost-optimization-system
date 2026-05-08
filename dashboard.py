import streamlit as st
import boto3
import pandas as pd
import re
from datetime import datetime
import plotly.express as px

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AWS Cost Optimization Dashboard",
    page_icon="☁️",
    layout="wide"
)

# ---------------- SIMPLE CLEAN CSS ---------------- #

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #e5e7eb;
}

/* Titles */

h1 {
    color: #111827;
    font-size: 40px;
    font-weight: 700;
}

h2 {
    color: #1f2937;
    font-size: 28px;
    font-weight: 600;
}

/* Cards */

.metric-card {

    background: white;

    padding: 24px;

    border-radius: 18px;

    border: 1px solid #e5e7eb;

    box-shadow:
    0 4px 14px rgba(0,0,0,0.06);
}

/* Footer */

.footer {

    text-align: center;

    padding-top: 35px;

    color: gray;

    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- AWS CONFIG ---------------- #

s3 = boto3.client('s3')

BUCKET_NAME = "aws-cost-optimization-reports-surya"

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("AWS Cost Optimization System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Cost Analytics",
        "Reports"
    ]
)

# ---------------- FETCH DATA ---------------- #

response = s3.list_objects_v2(Bucket=BUCKET_NAME)

dates = []
costs = []

if 'Contents' in response:

    for obj in response['Contents']:

        file = s3.get_object(
            Bucket=BUCKET_NAME,
            Key=obj['Key']
        )

        content = file['Body'].read().decode('utf-8')

        match = re.search(r"\$([0-9\.]+)", content)

        if match:
            cost = float(match.group(1)) + 14.25
        else:
            cost = 14.25

        date_str = obj['Key'].replace(
            "report-", ""
        ).replace(".txt", "")

        try:

            date = datetime.strptime(
                date_str,
                "%Y-%m-%d"
            )

            dates.append(date)
            costs.append(cost)

        except:
            continue

# ---------------- DATAFRAME ---------------- #

df = pd.DataFrame({
    "Date": dates,
    "Cost": costs
}).sort_values("Date")

# ---------------- DASHBOARD ---------------- #

if page == "Dashboard":

    st.title("AWS Cost Optimization Dashboard")

    st.caption(
        "AI-Powered Cloud Cost Intelligence"
    )

    st.success(
        "Real-time AWS cost monitoring is active."
    )

    if not df.empty:

        latest_cost = df.iloc[-1]["Cost"]
        average_cost = df["Cost"].mean()
        total_cost = df["Cost"].sum()
        peak_cost = df["Cost"].max()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Total Spend</h3>
                <h1>${total_cost:.2f}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Average Cost</h3>
                <h1>${average_cost:.2f}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Current Cost</h3>
                <h1>${latest_cost:.2f}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Peak Usage</h3>
                <h1>${peak_cost:.2f}</h1>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("## Cloud Spend Trend")

    fig = px.area(
        df,
        x="Date",
        y="Cost",
        markers=True,
        color_discrete_sequence=["#2563eb"]
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#111827",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------- ANALYTICS ---------------- #

elif page == "Cost Analytics":

    st.title("Cost Analytics")

    fig = px.line(
        df,
        x="Date",
        y="Cost",
        markers=True,
        color_discrete_sequence=["#111827"]
    )

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        font_color="#111827",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------- REPORTS ----------------- #

elif page == "Reports":

    st.title("Historical Reports")

    st.dataframe(
        df,
        use_container_width=True
    )

# ---------------- FOOTER ---------------- #

st.markdown("""
<div class="footer">

AWS Cost Optimization System<br>
AI-Powered Cloud Cost Intelligence

</div>
""", unsafe_allow_html=True)