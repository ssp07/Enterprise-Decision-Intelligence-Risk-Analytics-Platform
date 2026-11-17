import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_engine

st.set_page_config(
    page_title="Decision Intelligence",
    layout="wide"
)

engine = get_engine()

st.title("📈 Decision Intelligence Center")
st.markdown(
    "Monitor decision activity, decision costs, and strategic spending patterns."
)

# ==========================================
# KPI SECTION
# ==========================================

try:

    kpi = pd.read_sql("""
        SELECT
            COUNT(*) AS total_decisions,
            ROUND(AVG(estimated_cost),2) AS avg_cost,
            MAX(estimated_cost) AS max_cost,
            MIN(decision_date) AS first_decision,
            MAX(decision_date) AS latest_decision
        FROM fact_decision
    """, engine)

    total_decisions = int(kpi.iloc[0]["total_decisions"])
    avg_cost = float(kpi.iloc[0]["avg_cost"])
    max_cost = float(kpi.iloc[0]["max_cost"])

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Total Decisions",
        f"{total_decisions:,}"
    )

    c2.metric(
        "Average Cost",
        f"₹{avg_cost:,.0f}"
    )

    c3.metric(
        "Highest Cost",
        f"₹{max_cost:,.0f}"
    )

except Exception as e:
    st.error(f"KPI Error: {e}")

st.divider()

# ==========================================
# DECISION TREND
# ==========================================

try:

    trend = pd.read_sql("""
        SELECT
            decision_date,
            COUNT(*) AS decisions
        FROM fact_decision
        GROUP BY decision_date
        ORDER BY decision_date
    """, engine)

    st.subheader("📅 Decision Activity Trend")

    fig = px.line(
        trend,
        x="decision_date",
        y="decisions",
        title="Decision Trend Over Time",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

except Exception as e:
    st.error(f"Trend Error: {e}")

# ==========================================
# COST DISTRIBUTION
# ==========================================

try:

    cost_df = pd.read_sql("""
        SELECT estimated_cost
        FROM fact_decision
    """, engine)

    st.subheader("💰 Decision Cost Distribution")

    fig2 = px.histogram(
        cost_df,
        x="estimated_cost",
        nbins=30,
        title="Cost Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

except Exception as e:
    st.error(f"Cost Error: {e}")

# ==========================================
# COST BANDS
# ==========================================

try:

    bucket = pd.read_sql("""
        SELECT
        CASE
            WHEN estimated_cost < 100000 THEN 'Low Cost'
            WHEN estimated_cost < 500000 THEN 'Medium Cost'
            ELSE 'High Cost'
        END AS cost_band,
        COUNT(*) AS decisions
        FROM fact_decision
        GROUP BY cost_band
    """, engine)

    st.subheader("📊 Decision Cost Bands")

    fig3 = px.pie(
        bucket,
        names="cost_band",
        values="decisions",
        hole=.4
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

except Exception as e:
    st.error(f"Cost Band Error: {e}")

# ==========================================
# TOP 20 DECISIONS
# ==========================================

try:

    top_decisions = pd.read_sql("""
        SELECT
            decision_id,
            estimated_cost
        FROM fact_decision
        ORDER BY estimated_cost DESC
        LIMIT 20
    """, engine)

    st.subheader("🏆 Top 20 Most Expensive Decisions")

    st.dataframe(
        top_decisions,
        use_container_width=True
    )

except Exception as e:
    st.error(f"Top Decisions Error: {e}")

# ==========================================
# INSIGHTS
# ==========================================

st.subheader("🧠 Executive Findings")

st.success(
    f"""
• Organization recorded **{total_decisions:,} decisions**

• Average decision cost equals **₹{avg_cost:,.0f}**

• Highest cost decision reached **₹{max_cost:,.0f}**

• Decision activity data is actively being monitored
"""
)