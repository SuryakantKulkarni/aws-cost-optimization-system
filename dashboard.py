import streamlit as st
import boto3
import pandas as pd
import re
from datetime import datetime
import plotly.express as px

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="CloudCost AI",
    page_icon="☁️",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.main {
    background-color: #f4f7fb;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

section[data-testid="stSidebar"] {
    background: white;
    border-right: 1px solid #e5e7eb;
}

h1, h2, h3 {
    color: #111827;
}

.metric-card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 18px rgba(0,0,0,0.05);
}

.insight-card {
    background: linear-gradient(
        135deg,
        #ffffff,
        #f8fafc
    );

    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 4px 16px rgba(0,0,0,0.05);
}

.status-card {
    background: #ecfdf5;
    border: 1px solid #10b981;
    padding: 16px;
    border-radius: 14px;
    color: #065f46;
}

.footer {
    text-align: center;
    padding-top: 30px;
    color: gray;
}

</style>
""", unsafe_allow_html=True)

# ---------------- AWS CONFIG ---------------- #

s3 = boto3.client('s3')

BUCKET_NAME = "aws-cost-optimization-reports-surya"

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("☁️ CloudCost AI")

    st.markdown("---")

    st.markdown("### Platform Modules")

    st.write("📊 Executive Dashboard")
    st.write("💰 Cost Analytics")
    st.write("🚨 Smart Alerts")
    st.write("🤖 AI Recommendations")
    st.write("⚙️ Infrastructure Insights")
    st.write("📁 Historical Reports")

    st.markdown("---")

    st.markdown("""
    <div class="status-card">
        <b>System Status:</b><br>
        All AWS monitoring services operational.
    </div>
    """, unsafe_allow_html=True)

# ---------------- HEADER ---------------- #

st.markdown("""
# ☁️ CloudCost AI Dashboard

Enterprise-grade AWS cloud financial monitoring and optimization platform.
""")

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
            cost = float(match.group(1))
        else:
            cost = 0

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

# ---------------- TABS ---------------- #

tab1, tab2, tab3 = st.tabs([
    "📊 Overview",
    "🤖 AI Insights",
    "📁 Reports"
])

# ---------------- OVERVIEW TAB ---------------- #

with tab1:

    if not df.empty:

        latest_cost = df.iloc[-1]["Cost"]
        average_cost = df["Cost"].mean()
        total_cost = df["Cost"].sum()
        highest_cost = df["Cost"].max()

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.markdown(f"""
            <div class="metric-card">
                <h3>💰 Total Cost</h3>
                <h1>${total_cost:.2f}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col2:

            st.markdown(f"""
            <div class="metric-card">
                <h3>📈 Average Cost</h3>
                <h1>${average_cost:.2f}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col3:

            st.markdown(f"""
            <div class="metric-card">
                <h3>🚨 Latest Cost</h3>
                <h1>${latest_cost:.2f}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col4:

            st.markdown(f"""
            <div class="metric-card">
                <h3>🔥 Peak Cost</h3>
                <h1>${highest_cost:.2f}</h1>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("## 📊 AWS Cost Trend Analytics")

    fig = px.area(
        df,
        x="Date",
        y="Cost",
        markers=True
    )

    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font_color="#111827"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------- AI TAB ---------------- #

with tab2:

    st.markdown("## 🤖 AI Optimization Insights")

    col5, col6 = st.columns(2)

    if not df.empty:

        latest_cost = df.iloc[-1]["Cost"]
        average_cost = df["Cost"].mean()

        with col5:

            if latest_cost > average_cost:

                st.markdown("""
                <div class="insight-card">
                    <h3>⚠️ Cost Alert</h3>
                    <p>
                    AWS spending is above normal baseline.
                    Recommended actions:
                    </p>
                    <ul>
                        <li>Review unused EC2 instances</li>
                        <li>Optimize storage usage</li>
                        <li>Check idle services</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

            else:

                st.markdown("""
                <div class="insight-card">
                    <h3>✅ Infrastructure Healthy</h3>
                    <p>
                    Cloud spending patterns are optimized and stable.
                    </p>
                </div>
                """, unsafe_allow_html=True)

        with col6:

            if len(df) > 3:

                trend = df["Cost"].diff().mean()

                if trend > 5:

                    st.markdown("""
                    <div class="insight-card">
                        <h3>🚨 Trend Analysis</h3>
                        <p>
                        Increasing infrastructure cost trend detected.
                        Long-term optimization recommended.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                else:

                    st.markdown("""
                    <div class="insight-card">
                        <h3>📊 Usage Pattern</h3>
                        <p>
                        Resource utilization appears balanced and healthy.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

    st.markdown("## 🎯 Optimization Recommendations")

    st.info("💡 Consider Reserved Instances for predictable workloads.")
    st.info("💡 Enable S3 lifecycle policies for unused storage.")
    st.info("💡 Monitor Lambda execution frequency regularly.")

# ---------------- REPORTS TAB ---------------- #

with tab3:

    st.markdown("## 📁 Historical Cost Reports")

    st.dataframe(
        df,
        use_container_width=True
    )

# ---------------- FOOTER ---------------- #

st.markdown("""
<div class="footer">
Built with AWS • Streamlit • Python • DevOps Automation
</div>
""", unsafe_allow_html=True)