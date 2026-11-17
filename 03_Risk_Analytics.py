import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_engine

engine = get_engine()

st.title("⚠️ Risk Intelligence Center")

# KPIs

risk_kpi = pd.read_sql("""
SELECT
COUNT(*) total_risks,
ROUND(AVG(probability),2) avg_probability,
ROUND(AVG(impact),2) avg_impact
FROM fact_risk_assessment
""", engine)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total Risks",
    int(risk_kpi["total_risks"][0])
)

c2.metric(
    "Avg Probability",
    risk_kpi["avg_probability"][0]
)

c3.metric(
    "Avg Impact",
    risk_kpi["avg_impact"][0]
)

st.divider()

# Impact Distribution

impact = pd.read_sql("""
SELECT
impact,
COUNT(*) cnt
FROM fact_risk_assessment
GROUP BY impact
ORDER BY impact
""", engine)

fig = px.bar(
    impact,
    x="impact",
    y="cnt",
    title="Risk Impact Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# Heatmap

heat = pd.read_sql("""
SELECT
probability,
impact
FROM fact_risk_assessment
LIMIT 3000
""", engine)

fig2 = px.density_heatmap(
    heat,
    x="probability",
    y="impact",
    title="Risk Heatmap"
)

st.plotly_chart(fig2, use_container_width=True)

# Scatter

fig3 = px.scatter(
    heat,
    x="probability",
    y="impact",
    title="Probability vs Impact"
)

st.plotly_chart(fig3, use_container_width=True)

st.warning("""
RISK INSIGHT

High impact risks (8-10) should receive immediate attention.
Probability and impact together determine risk severity.
""")