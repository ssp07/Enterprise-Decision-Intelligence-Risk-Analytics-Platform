import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_engine

engine = get_engine()

st.set_page_config(
    page_title="Financial Performance",
    layout="wide"
)

st.title("💰 Financial Performance")

# ===================================
# KPIs
# ===================================

financials = pd.read_sql("""
SELECT
COALESCE(SUM(actual_benefit),0) total_benefit,
COALESCE(SUM(actual_cost),0) total_cost,
COALESCE(
SUM(actual_benefit - actual_cost),0
) total_profit
FROM fact_decision_outcome
""", engine)

benefit = float(financials.iloc[0]["total_benefit"])
cost = float(financials.iloc[0]["total_cost"])
profit = float(financials.iloc[0]["total_profit"])

roi = 0

if cost > 0:
    roi = round((profit / cost) * 100, 2)

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Total Benefit",
    f"₹{benefit:,.0f}"
)

c2.metric(
    "Total Cost",
    f"₹{cost:,.0f}"
)

c3.metric(
    "Profit",
    f"₹{profit:,.0f}"
)

c4.metric(
    "ROI %",
    f"{roi}%"
)

st.divider()

# ===================================
# BENEFIT VS COST
# ===================================

comparison = pd.read_sql("""
SELECT
decision_id,
actual_benefit,
actual_cost
FROM fact_decision_outcome
LIMIT 1000
""", engine)

fig = px.scatter(
    comparison,
    x="actual_cost",
    y="actual_benefit",
    title="Benefit vs Cost"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ===================================
# PROFIT DISTRIBUTION
# ===================================

profit_dist = pd.read_sql("""
SELECT
(actual_benefit - actual_cost) profit
FROM fact_decision_outcome
""", engine)

fig2 = px.histogram(
    profit_dist,
    x="profit",
    nbins=30,
    title="Profit Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ===================================
# TOP PROFITABLE DECISIONS
# ===================================

top_profit = pd.read_sql("""
SELECT
decision_id,
actual_benefit,
actual_cost,
(actual_benefit - actual_cost) profit
FROM fact_decision_outcome
ORDER BY profit DESC
LIMIT 20
""", engine)

st.subheader("🏆 Top 20 Most Profitable Decisions")

st.dataframe(
    top_profit,
    use_container_width=True
)

# ===================================
# FINDINGS
# ===================================

st.subheader("🧠 Financial Findings")

st.success(f"""
Total benefit generated is ₹{benefit:,.0f}.

The organization generated net profit of ₹{profit:,.0f}.

Portfolio ROI currently stands at {roi}%.
""")