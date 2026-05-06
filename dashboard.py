import streamlit as st
import boto3
import pandas as pd
import re
from datetime import datetime
import plotly.express as px

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AWS Cost Optimization Platform",
    page_icon="☁️",
    layout="wide"
)

# ---------------- PREMIUM UI CSS ---------------- #

st.markdown("""
<style>

* {
    transition: all 0.25s ease-in-out;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main {
    background: linear-gradient(
        135deg,
        #eef4ff,
        #f8fbff,
        #ffffff
    );
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

/* ---------------- SIDEBAR ---------------- */

section[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #1d4ed8,
        #3b82f6
    );

    border-right: none;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ---------------- TITLES ---------------- */

h1 {
    color: #0f172a;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1px;
}

h2 {
    color: #1e293b;
    font-size: 28px;
    font-weight: 700;
}

h3 {
    color: #334155;
    font-weight: 600;
}

/* ---------------- KPI CARDS ---------------- */

.metric-card {

    background: linear-gradient(
        135deg,
        #2563eb,
        #3b82f6
    );

    padding: 24px;

    border-radius: 22px;

    color: white;

    backdrop-filter: blur(10px);

    border-top: 4px solid rgba(255,255,255,0.5);

    box-shadow:
    0 10px 25px rgba(37, 99, 235, 0.18);
}

.metric-card:hover {

    transform:
    translateY(-6px)
    scale(1.01);

    box-shadow:
    0 16px 35px rgba(37,99,235,0.22);
}

.metric-card h1,
.metric-card h3 {
    color: white !important;
}

/* ---------------- INSIGHT CARDS ---------------- */

.insight-card {

    background: white;

    padding: 24px;

    border-radius: 22px;

    border-left: 6px solid #2563eb;

    box-shadow:
    0 8px 24px rgba(15, 23, 42, 0.08);
}

.insight-card:hover {
    transform: translateY(-4px);
}

/* ---------------- TEXT ---------------- */

.small-text {
    color: #475569;
    font-size: 15px;
}

/* ---------------- TABS ---------------- */

.stTabs [data-baseweb="tab"] {

    font-size: 16px;
    font-weight: 600;

    color: #2563eb;

    background-color: white;

    border-radius: 12px;

    padding: 10px 18px;

    margin-right: 8px;

    border: 1px solid #dbeafe;
}

.stTabs [aria-selected="true"] {

    background: linear-gradient(
        135deg,
        #2563eb,
        #3b82f6
    );

    color: white !important;

    border: none;
}

/* ---------------- TABLE ---------------- */

.stDataFrame {

    border-radius: 18px;

    overflow: hidden;

    border: 1px solid #dbeafe;
}

/* ---------------- FOOTER ---------------- */

.footer {

    text-align: center;

    padding-top: 35px;

    color: #64748b;

    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- AWS CONFIG ---------------- #

s3 = boto3.client('s3')

BUCKET_NAME = "aws-cost-optimization-reports-surya"

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("AWS Cost")
    st.title("Optimization Platform")

    st.markdown(
        "<p class='small-text'>AI-Powered Cloud Cost Intelligence</p>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "Executive Dashboard",
            "Cost Analytics",
            "AI Insights",
            "Historical Reports"
        ]
    )

    st.markdown("---")

    st.success("Monitoring Services Operational")

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

# ---------------- EXECUTIVE DASHBOARD ---------------- #

if page == "Executive Dashboard":

    st.title("AWS Cost Optimization Platform")

    st.markdown(
        "<p class='small-text'>Real-time cloud financial operations and optimization dashboard.</p>",
        unsafe_allow_html=True
    )

    st.info(
        "AI-powered AWS cloud cost monitoring and optimization platform is active."
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
                <h3>Total Cloud Spend</h3>
                <h1 style='font-size:42px;font-weight:800;'>
                ${total_cost:.2f}
                </h1>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Average Cost</h3>
                <h1 style='font-size:42px;font-weight:800;'>
                ${average_cost:.2f}
                </h1>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Current Billing</h3>
                <h1 style='font-size:42px;font-weight:800;'>
                ${latest_cost:.2f}
                </h1>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Peak Usage</h3>
                <h1 style='font-size:42px;font-weight:800;'>
                ${peak_cost:.2f}
                </h1>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("## Cloud Spend Analytics")

    fig = px.area(
        df,
        x="Date",
        y="Cost",
        markers=True,
        color_discrete_sequence=["#2563eb"]
    )

    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font_color="#111827",
        title_font_size=24,
        hovermode="x unified"
    )

    fig.update_traces(
        line=dict(width=4),
        marker=dict(size=9)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------- COST ANALYTICS ---------------- #

elif page == "Cost Analytics":

    st.title("Cost Analytics")

    fig = px.line(
        df,
        x="Date",
        y="Cost",
        markers=True,
        color_discrete_sequence=["#0f172a"]
    )

    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font_color="#111827",
        title_font_size=24,
        hovermode="x unified"
    )

    fig.update_traces(
        line=dict(width=4),
        marker=dict(size=9)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        df,
        use_container_width=True
    )

# ---------------- AI INSIGHTS ---------------- #

elif page == "AI Insights":

    st.title("AI Optimization Insights")

    if not df.empty:

        latest_cost = df.iloc[-1]["Cost"]
        average_cost = df["Cost"].mean()

        col1, col2 = st.columns(2)

        with col1:

            if latest_cost > average_cost:

                st.markdown("""
                <div class="insight-card">

                    <h3>Cost Increase Detected</h3>

                    <p>
                    AWS spending is above normal baseline.
                    Recommended optimization review required.
                    </p>

                    <ul>
                        <li>Review idle EC2 instances</li>
                        <li>Optimize S3 lifecycle policies</li>
                        <li>Analyze Lambda execution frequency</li>
                    </ul>

                </div>
                """, unsafe_allow_html=True)

            else:

                st.markdown("""
                <div class="insight-card">

                    <h3>Infrastructure Optimized</h3>

                    <p>
                    AWS infrastructure cost pattern is healthy and stable.
                    </p>

                </div>
                """, unsafe_allow_html=True)

        with col2:

            st.markdown("""
            <div class="insight-card">

                <h3>Optimization Recommendations</h3>

                <ul>
                    <li>Enable Reserved Instances</li>
                    <li>Monitor unused services</li>
                    <li>Track monthly billing trends</li>
                    <li>Review storage utilization</li>

                </ul>

            </div>
            """, unsafe_allow_html=True)

# ---------------- REPORTS ---------------- #

elif page == "Historical Reports":

    st.title("Historical Reports")

    st.dataframe(
        df,
        use_container_width=True
    )

# ---------------- FOOTER ---------------- #

st.markdown("""
<div class="footer">

<b>AWS Cost Optimization Platform</b><br>

AI-Powered Cloud Cost Intelligence Platform<br><br>

Built using AWS Lambda • S3 • EC2 • EventBridge • Streamlit

</div>
""", unsafe_allow_html=True)