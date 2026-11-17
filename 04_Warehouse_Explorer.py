import streamlit as st
import pandas as pd

from utils.db import get_engine

engine = get_engine()

st.title("🗄️ Warehouse Explorer")

tables = pd.read_sql("""
SELECT table_name
FROM information_schema.tables
WHERE table_schema='public'
ORDER BY table_name
""", engine)

selected = st.selectbox(
    "Select Table",
    tables["table_name"]
)

st.subheader(f"Preview : {selected}")

df = pd.read_sql(
    f"SELECT * FROM {selected} LIMIT 100",
    engine
)

st.dataframe(
    df,
    use_container_width=True
)

st.subheader("Table Statistics")

c1, c2 = st.columns(2)

c1.metric(
    "Rows Displayed",
    len(df)
)

c2.metric(
    "Columns",
    len(df.columns)
)

st.download_button(
    "⬇ Download CSV",
    df.to_csv(index=False),
    f"{selected}.csv",
    "text/csv"
)