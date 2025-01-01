# pages/credit_status.py

import streamlit as st
import plotly.express as px
from utils.database import execute_query
from utils.database import get_database_connection
from config import setup_page

setup_page()

try:
    engine = get_database_connection()
    st.sidebar.success("📊 Connected to database!")
except Exception as e:
    st.error(f"Error connecting to database: {str(e)}")
    st.stop()
st.title("📈 Credit Status Analysis")

# Status trends over time
st.subheader("Credit Status Trends Over Time")
status_trend = execute_query(engine, """
    SELECT 
        months_balance,
        status,
        COUNT(*) as count
    FROM credit_record
    GROUP BY months_balance, status
    ORDER BY months_balance
""")

if not status_trend.empty:
    fig = px.line(
        status_trend, 
        x='months_balance', 
        y='count', 
        color='status',
        title='Credit Status Trends Over Time',
        labels={'months_balance': 'Months Balance', 'count': 'Number of Records'},
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for Credit Status Trends Over Time.")

# Status transition matrix
st.subheader("Status Transition Analysis")
transitions = execute_query(engine, """
    WITH status_changes AS (
        SELECT 
            id,
            status as current_status,
            LEAD(status) OVER (PARTITION BY id ORDER BY months_balance) as next_status
        FROM credit_record
    )
    SELECT 
        current_status,
        next_status,
        COUNT(*) as transitions
    FROM status_changes
    WHERE next_status IS NOT NULL
    GROUP BY current_status, next_status
    ORDER BY current_status, next_status
""")

if not transitions.empty:
    pivot_transitions = transitions.pivot(index='current_status', columns='next_status', values='transitions').fillna(0)
    
    fig = px.imshow(
        pivot_transitions,
        labels=dict(x="Next Status", y="Current Status", color="Number of Transitions"),
        x=pivot_transitions.columns,
        y=pivot_transitions.index,
        color_continuous_scale='Blues',
        title='Credit Status Transition Matrix'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for Status Transition Analysis.")
