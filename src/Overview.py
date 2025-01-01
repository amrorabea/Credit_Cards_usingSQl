import streamlit as st

from utils.database import get_database_connection
from utils.database import execute_query
import plotly.express as px
from config import setup_page
from utils.helpers import format_currency

setup_page()

try:
    engine = get_database_connection()
    st.sidebar.success("📊 Connected to database!")
except Exception as e:
    st.error(f"Error connecting to database: {str(e)}")
    st.stop()
st.title("📊 Credit Analysis Overview")
    
# Key metrics in columns
col1, col2, col3, col4 = st.columns(4)

# Total clients
total_clients_df = execute_query(engine, "SELECT COUNT(DISTINCT id) as count FROM client_data")
total_clients = total_clients_df.iloc[0]['count'] if not total_clients_df.empty else 0
col1.metric("Total Clients", f"{total_clients:,}")

# Average income
avg_income_df = execute_query(engine, "SELECT AVG(amt_income_total) as avg_income FROM client_data")
avg_income = avg_income_df.iloc[0]['avg_income'] if not avg_income_df.empty else 0
col2.metric("Average Income", format_currency(avg_income))

# Total credit records
total_records_df = execute_query(engine, "SELECT COUNT(*) as count FROM credit_record")
total_records = total_records_df.iloc[0]['count'] if not total_records_df.empty else 0
col3.metric("Total Credit Records", f"{total_records:,}")

# Clients with problems (status not in 'C', '0', 'X')
problem_clients_df = execute_query(engine, """
    SELECT COUNT(DISTINCT id) as count 
    FROM credit_record 
    WHERE status NOT IN ('C', '0', 'X')
""")
problem_clients = problem_clients_df.iloc[0]['count'] if not problem_clients_df.empty else 0
col4.metric("Clients with Issues", f"{problem_clients:,}")

# Credit status distribution
st.subheader("Credit Status Distribution")
status_dist = execute_query(engine, """
    SELECT status, COUNT(*) as count 
    FROM credit_record 
    GROUP BY status 
    ORDER BY count DESC
""")

if not status_dist.empty:
    fig = px.pie(status_dist, values='count', names='status', title='Credit Status Distribution')
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for Credit Status Distribution.")

# Income type and credit status
st.subheader("Income Type vs Credit Status")
income_status = execute_query(engine, """
    SELECT c.name_income_type, cr.status, COUNT(*) as count
    FROM client_data c
    JOIN credit_record cr ON c.id = cr.id
    GROUP BY c.name_income_type, cr.status
    ORDER BY count DESC
""")

if not income_status.empty:
    fig = px.treemap(
        income_status, 
        path=['name_income_type', 'status'],
        values='count',
        title='Income Type and Credit Status Distribution'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for Income Type vs Credit Status.")