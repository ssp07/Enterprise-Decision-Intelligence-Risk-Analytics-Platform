import streamlit as st
import pandas as pd

from utils.db import get_engine

engine = get_engine()

st.title("💻 SQL Query Runner")

query = st.text_area(
    "Enter SQL Query",
    height=200,
    value="""
SELECT *
FROM fact_decision
LIMIT 100
"""
)

c1, c2 = st.columns(2)

if c1.button("▶ Execute Query"):

    try:

        result = pd.read_sql(
            query,
            engine
        )

        st.success(
            f"{len(result)} rows returned"
        )

        st.dataframe(
            result,
            use_container_width=True
        )

        st.download_button(
            "Download Results",
            result.to_csv(index=False),
            "query_results.csv",
            "text/csv"
        )

    except Exception as e:

        st.error(str(e))

if c2.button("Sample Queries"):

    st.code("""
-- Decisions

SELECT *
FROM fact_decision
LIMIT 10;

-- Risks

SELECT *
FROM fact_risk_assessment
LIMIT 10;

-- Outcomes

SELECT *
FROM fact_decision_outcome
LIMIT 10;

-- Top Costs

SELECT *
FROM fact_decision
ORDER BY estimated_cost DESC
LIMIT 20;
""")