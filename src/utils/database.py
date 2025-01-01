import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from dotenv import load_dotenv

@st.cache_resource
def get_database_connection():
    load_dotenv()
    connection_string = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    return create_engine(connection_string)

@st.cache_data
def execute_query(_engine, query):
    return pd.read_sql_query(query, _engine)