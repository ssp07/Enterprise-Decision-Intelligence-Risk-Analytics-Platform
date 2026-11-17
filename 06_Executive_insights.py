import streamlit as st
import pandas as pd

from utils.db import get_engine

engine = get_engine()

st.set_page_config(
    page_title="Executive Insights",
    layout="wide"
)

st.title("🧠 Executive Intelligence Center")
st.markdown(
    "Organization-wide performance indicators and recommendations."
)

# =======================================
# LOAD METRICS
# =======================================

decisions = pd.read_sql(
"""
SELECT COUNT(*) total
FROM fact_decision
""",
engine
).iloc[0,0]

risks = pd.read_sql(
"""
SELECT COUNT(*)
FROM fact_risk_assessment
WHERE impact >= 8
""",
engine
).iloc[0,0]

success = pd.read_sql(
"""
SELECT ROUND(AVG(success_rating),2)
FROM fact_decision_outcome
""",
engine
).iloc[0,0]

avg_cost = pd.read_sql(
"""
SELECT ROUND(AVG(estimated_cost),2)
FROM fact_decision
""",
engine
).iloc[0,0]

# =======================================
# HEALTH SCORE
# =======================================

health_score = max(
    0,
    min(
        100,
        round(
            (success * 10)
            -
            ((risks / decisions) * 100)
        )
    )
)

# =======================================
# KPI SECTION
# =======================================

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Decisions",
    f"{decisions:,}"
)

c2.metric(
    "Critical Risks",
    f"{risks:,}"
)

c3.metric(
    "Success Score",
    f"{success}/10"
)

c4.metric(
    "Health Score",
    f"{health_score}/100"
)

st.progress(
    health_score / 100
)

st.divider()

# =======================================
# KEY FINDINGS
# =======================================

st.subheader("🔍 Key Findings")

st.success(
    f"""
Organization processed **{decisions:,} strategic decisions**.
"""
)

st.warning(
    f"""
**{risks:,} high-impact risks**
require active monitoring.
"""
)

st.info(
    f"""
Average success level is
**{success}/10**.
"""
)

# =======================================
# EXECUTIVE ALERTS
# =======================================

st.subheader("🚨 Executive Alerts")

if risks > 250:
    st.error(
        "Critical risk volume exceeds recommended threshold."
    )

if success < 6:
    st.warning(
        "Decision effectiveness is below target performance."
    )

if decisions > 1000:
    st.success(
        "Decision warehouse adoption remains healthy."
    )

# =======================================
# EXECUTIVE SUMMARY
# =======================================

st.subheader("📋 Executive Summary")

st.markdown(f"""
- Organization processed **{decisions:,} decisions**
- Average decision success is **{success}/10**
- Average decision spend is **₹{avg_cost:,.0f}**
- High-impact risks count stands at **{risks:,}**
- Analytics warehouse is successfully connected
- Executive intelligence reporting is operational
""")

# =======================================
# RECOMMENDATIONS
# =======================================

st.subheader("🎯 Executive Recommendations")

recommendations = []

if success < 6:
    recommendations.append(
        "Review decision governance and approval workflows."
    )

if risks > decisions * 0.20:
    recommendations.append(
        "Increase focus on risk mitigation planning."
    )

if avg_cost > 300000:
    recommendations.append(
        "Evaluate spending effectiveness and ROI."
    )

if not recommendations:
    recommendations.append(
        "Current organization indicators remain within healthy thresholds."
    )

for item in recommendations:
    st.markdown(f"✅ {item}")

# =======================================
# ORGANIZATIONAL STATUS
# =======================================

st.subheader("🏢 Organizational Status")

if health_score >= 80:
    st.success("Organization status: HEALTHY")

elif health_score >= 60:
    st.warning("Organization status: STABLE")

else:
    st.error("Organization status: REQUIRES ATTENTION")