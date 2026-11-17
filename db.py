from sqlalchemy import create_engine
import streamlit as st


@st.cache_resource
def get_engine():

    host = st.secrets["host"]
    port = st.secrets["port"]
    database = st.secrets["database"]
    user = st.secrets["user"]
    password = st.secrets["password"]

    return create_engine(
        f"postgresql+psycopg://{user}:{password}@{host}:{port}/{database}"
    )