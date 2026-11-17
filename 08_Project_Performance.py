import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import get_engine

engine = get_engine()

st.set_page_config(
    page_title="Project Performance",
    layout="wide"
)

st.title("📊 Project Performance")

# ===================================
# PROJECT KPIS
# ===================================

project_count = pd.read_sql("""
SELECT COUNT(*) total
FROM dim_project
""", engine).iloc[0,0]

activity = pd.read_sql("""
SELECT
project_id,
COUNT(*) decisions,
AVG(estimated_cost) avg_cost
FROM fact_decision
GROUP BY project_id
ORDER BY decisions DESC
""", engine)

most_active_project = (
    activity.iloc[0]["project_id"]
    if not activity.empty
    else "N/A"
)

avg_project_cost = (
    activity["avg_cost"].mean()
    if not activity.empty
    else 0
)

c1,c2,c3 = st.columns(3)

c1.metric(
    "Projects",
    int(project_count)
)

c2.metric(
    "Most Active Project",
    int(most_active_project)
)

c3.metric(
    "Avg Project Cost",
    f"₹{avg_project_cost:,.0f}"
)

st.divider()

# ===================================
# TOP PROJECTS
# ===================================

top_projects = activity.head(20)

fig = px.bar(
    top_projects,
    x="project_id",
    y="decisions",
    title="Top Projects by Decision Count",
    color="decisions"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ===================================
# TREEMAP
# ===================================

fig2 = px.treemap(
    top_projects,
    path=["project_id"],
    values="decisions",
    title="Project Activity Treemap"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ===================================
# COST ANALYSIS
# ===================================

fig3 = px.scatter(
    activity.head(100),
    x="decisions",
    y="avg_cost",
    title="Project Cost vs Activity"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ===================================
# FINDINGS
# ===================================

st.subheader("🧠 Project Insights")

st.info(f"""
Project {most_active_project}
currently generates the highest activity.

The top projects contribute a significant
portion of organizational decisions.
""")