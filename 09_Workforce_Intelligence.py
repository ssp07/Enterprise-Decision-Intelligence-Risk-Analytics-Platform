import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_engine

engine = get_engine()

st.set_page_config(
    page_title="Workforce Intelligence",
    layout="wide"
)

st.title("👥 Workforce Intelligence")

# ===================================
# EMPLOYEE KPIS
# ===================================

employees = pd.read_sql("""
SELECT COUNT(*) total
FROM dim_employee
""", engine)

total_employees = int(employees.iloc[0,0])

activity = pd.read_sql("""
SELECT
employee_id,
COUNT(*) decisions
FROM fact_decision
GROUP BY employee_id
ORDER BY decisions DESC
""", engine)

if activity.empty:

    st.warning(
        "No employee activity data found."
    )

    st.stop()

top_employee = int(activity.iloc[0]["employee_id"])

avg_decisions = round(
    activity["decisions"].mean(),
    2
)

c1,c2,c3 = st.columns(3)

c1.metric(
    "Employees",
    total_employees
)

c2.metric(
    "Top Contributor",
    top_employee
)

c3.metric(
    "Avg Decisions",
    avg_decisions
)

st.divider()

# ===================================
# TOP CONTRIBUTOR CHART
# ===================================

top20 = activity.head(20)

fig = px.bar(
    top20,
    x="employee_id",
    y="decisions",
    color="decisions",
    title="Top 20 Contributors"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ===================================
# DISTRIBUTION
# ===================================

fig2 = px.histogram(
    activity,
    x="decisions",
    nbins=20,
    title="Decision Participation Distribution"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ===================================
# LEADERBOARD
# ===================================

st.subheader("🏆 Workforce Leaderboard")

st.dataframe(
    top20,
    use_container_width=True
)

# ===================================
# INSIGHTS
# ===================================

top_share = round(
    (
        top20["decisions"].sum()
        /
        activity["decisions"].sum()
    ) * 100,
    2
)

st.subheader("🧠 Workforce Insights")

st.success(f"""
Top 20 contributors account for
{top_share}% of all decision activity.

Employee participation remains active
across the decision ecosystem.

Employee {top_employee}
currently leads organizational activity.
""")