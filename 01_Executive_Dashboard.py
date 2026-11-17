import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_engine

engine = get_engine()

st.set_page_config(
    page_title="Executive Dashboard",
    layout="wide"
)

st.title("🏢 Executive Command Center")

st.markdown(
    "Enterprise Decision Intelligence & Risk Analytics Platform"
)

# =======================================
# DATE FILTER
# =======================================

date_range = pd.read_sql("""
SELECT
MIN(decision_date) min_date,
MAX(decision_date) max_date
FROM fact_decision
""", engine)

min_date = date_range.iloc[0]["min_date"]
max_date = date_range.iloc[0]["max_date"]

selected_dates = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date)
)

start_date = selected_dates[0]
end_date = selected_dates[1]

# =======================================
# CORE METRICS
# =======================================

decision_metrics = pd.read_sql(f"""
SELECT
COUNT(*) total_decisions,
COALESCE(AVG(estimated_cost),0) avg_cost
FROM fact_decision
WHERE decision_date BETWEEN '{start_date}'
AND '{end_date}'
""", engine)

outcome_metrics = pd.read_sql("""
SELECT
COUNT(*) total_outcomes,
COALESCE(AVG(success_rating),0) avg_success
FROM fact_decision_outcome
""", engine)

risk_metrics = pd.read_sql("""
SELECT
COUNT(*) total_risks,
COUNT(*) FILTER (
WHERE impact >= 8
) critical_risks
FROM fact_risk_assessment
""", engine)

financial_metrics = pd.read_sql("""
SELECT
COALESCE(SUM(actual_benefit),0) benefit,
COALESCE(SUM(actual_cost),0) cost
FROM fact_decision_outcome
""", engine)

decisions = int(decision_metrics.iloc[0]["total_decisions"])
avg_cost = float(decision_metrics.iloc[0]["avg_cost"])

benefit = float(financial_metrics.iloc[0]["benefit"])
cost = float(financial_metrics.iloc[0]["cost"])

profit = benefit - cost

success_score = float(
    outcome_metrics.iloc[0]["avg_success"]
)

critical_risks = int(
    risk_metrics.iloc[0]["critical_risks"]
)

# =======================================
# HEALTH SCORE
# =======================================

if decisions > 0:

    health_score = max(
        0,
        min(
            100,
            round(
                (success_score * 10)
                -
                ((critical_risks / decisions) * 100)
            )
        )
    )

else:

    health_score = 0

# =======================================
# KPI SECTION
# =======================================

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric(
    "Health Score",
    f"{health_score}/100"
)

c2.metric(
    "Decisions",
    f"{decisions:,}"
)

c3.metric(
    "Critical Risks",
    f"{critical_risks:,}"
)

c4.metric(
    "Success Score",
    f"{success_score:.2f}/10"
)

c5.metric(
    "Profit",
    f"₹{profit:,.0f}"
)

st.progress(
    health_score / 100
)

st.divider()

# =======================================
# DECISION TREND
# =======================================

trend = pd.read_sql(f"""
SELECT
decision_date,
COUNT(*) decisions
FROM fact_decision
WHERE decision_date BETWEEN '{start_date}'
AND '{end_date}'
GROUP BY decision_date
ORDER BY decision_date
""", engine)

# =======================================
# SUCCESS DISTRIBUTION
# =======================================

success_dist = pd.read_sql("""
SELECT
success_rating,
COUNT(*) cnt
FROM fact_decision_outcome
GROUP BY success_rating
ORDER BY success_rating
""", engine)

left,right = st.columns(2)

with left:

    fig1 = px.line(
        trend,
        x="decision_date",
        y="decisions",
        title="Decision Activity Trend",
        markers=True
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with right:

    fig2 = px.bar(
        success_dist,
        x="success_rating",
        y="cnt",
        color="cnt",
        title="Success Score Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =======================================
# BENEFIT VS COST
# =======================================

compare = pd.read_sql("""
SELECT
actual_cost,
actual_benefit
FROM fact_decision_outcome
LIMIT 2000
""", engine)

fig3 = px.scatter(
    compare,
    x="actual_cost",
    y="actual_benefit",
    title="Benefit vs Cost"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# =======================================
# EXECUTIVE INSIGHTS
# =======================================

st.subheader("🧠 Executive Findings")

insights = []

if health_score >= 80:
    insights.append(
        "Organization health is performing at a strong level."
    )

elif health_score >= 60:
    insights.append(
        "Organization health remains stable but should be monitored."
    )

else:
    insights.append(
        "Organization health requires executive attention."
    )

if critical_risks > 250:
    insights.append(
        "Critical risk volume exceeds recommended thresholds."
    )

if success_score < 6:
    insights.append(
        "Decision success performance is below target."
    )

if profit > 0:
    insights.append(
        "Decision portfolio remains financially profitable."
    )

for item in insights:
    st.info(item)

# =======================================
# SUMMARY
# =======================================

st.subheader("📋 Executive Summary")

st.markdown(f"""
- Total decisions processed: **{decisions:,}**
- Critical risks identified: **{critical_risks:,}**
- Average success score: **{success_score:.2f}/10**
- Total benefit generated: **₹{benefit:,.0f}**
- Total cost incurred: **₹{cost:,.0f}**
- Net profit: **₹{profit:,.0f}**
- Organization health score: **{health_score}/100**
""")