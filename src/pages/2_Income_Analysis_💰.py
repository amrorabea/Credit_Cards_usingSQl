# pages/income_analysis.py

import streamlit as st
import plotly.express as px
from utils.database import execute_query
from config import setup_page
from utils.database import get_database_connection

setup_page()

try:
    engine = get_database_connection()
    st.sidebar.success("📊 Connected to database!")
except Exception as e:
    st.error(f"Error connecting to database: {str(e)}")
    st.stop()

st.title("💰 Income Analysis")

# Income distribution by type
st.subheader("Income Distribution by Type")
income_data = execute_query(engine, """
    SELECT name_income_type, amt_income_total
    FROM client_data
    WHERE amt_income_total IS NOT NULL
""")

if not income_data.empty:
    fig = px.box(
        income_data,
        x='name_income_type',
        y='amt_income_total',
        title='Income Distribution by Type',
        labels={'name_income_type': 'Income Type', 'amt_income_total': 'Income Amount'},
        color='name_income_type',
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for Income Distribution by Type.")

# Income vs Credit Status
st.subheader("Income Level Impact on Credit Status")
income_credit = execute_query(engine, """
    SELECT 
        CASE 
            WHEN amt_income_total < 50000 THEN 'Low Income'
            WHEN amt_income_total < 100000 THEN 'Middle Income'
            WHEN amt_income_total < 200000 THEN 'High Income'
            ELSE 'Very High Income'
        END as income_category,
        cr.status,
        COUNT(*) as count
    FROM client_data c
    JOIN credit_record cr ON c.id = cr.id
    GROUP BY income_category, cr.status
    ORDER BY count DESC
""")

if not income_credit.empty:
    fig = px.treemap(
        income_credit,
        path=['income_category', 'status'],
        values='count',
        title='Income Level and Credit Status Distribution',
        color='income_category',
        color_discrete_sequence=px.colors.sequential.Inferno
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for Income Level Impact on Credit Status.")
