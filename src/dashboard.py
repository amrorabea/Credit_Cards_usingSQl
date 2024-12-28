import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
import numpy as np

# Configure page
st.set_page_config(page_title="Credit Analysis Dashboard", layout="wide", initial_sidebar_state="expanded")

# Database connection configuration
DB_CONFIG = {
    "dbname": "bank",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": "5432"
}

# Create database connection
@st.cache_resource
def get_database_connection():
    connection_string = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
    return create_engine(connection_string)

# Cache for SQL queries
@st.cache_data
def execute_query(_engine, query):
    return pd.read_sql_query(query, _engine)

try:
    engine = get_database_connection()
    st.sidebar.success("📊 Connected to database!")
except Exception as e:
    st.error(f"Error connecting to database: {str(e)}")
    st.stop()

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page",
    ["Overview", "Client Demographics", "Income Analysis", "Credit Status", "Educational Impact", "Custom Analysis"]
)

# Helper function for formatting currency
def format_currency(value):
    return f"${value:,.2f}"

if page == "Overview":
    st.title("📊 Credit Analysis Overview")
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    # Total clients
    total_clients = execute_query(engine, "SELECT COUNT(DISTINCT id) as count FROM client_data").iloc[0]['count']
    col1.metric("Total Clients", f"{total_clients:,}")
    
    # Average income
    avg_income = execute_query(engine, "SELECT AVG(amt_income_total) as avg_income FROM client_data").iloc[0]['avg_income']
    col2.metric("Average Income", format_currency(avg_income))
    
    # Total credit records
    total_records = execute_query(engine, "SELECT COUNT(*) as count FROM credit_record").iloc[0]['count']
    col3.metric("Total Credit Records", f"{total_records:,}")
    
    # Clients with problems (status > 0)
    problem_clients = execute_query(engine, """
        SELECT COUNT(DISTINCT id) as count 
        FROM credit_record 
        WHERE status NOT IN ('C', '0', 'X')
    """).iloc[0]['count']
    col4.metric("Clients with Issues", f"{problem_clients:,}")
    
    # Credit status distribution
    st.subheader("Credit Status Distribution")
    status_dist = execute_query(engine, """
        SELECT status, COUNT(*) as count 
        FROM credit_record 
        GROUP BY status 
        ORDER BY count DESC
    """)
    fig = px.pie(status_dist, values='count', names='status', title='Credit Status Distribution')
    st.plotly_chart(fig, use_container_width=True)
    
    # Income type and credit status
    st.subheader("Income Type vs Credit Status")
    income_status = execute_query(engine, """
        SELECT c.name_income_type, cr.status, COUNT(*) as count
        FROM client_data c
        JOIN credit_record cr ON c.id = cr.id
        GROUP BY c.name_income_type, cr.status
        ORDER BY count DESC
    """)
    fig = px.treemap(income_status, 
                    path=['name_income_type', 'status'],
                    values='count',
                    title='Income Type and Credit Status Distribution')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Client Demographics":
    st.title("👥 Client Demographics Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gender distribution
        gender_dist = execute_query(engine, """
            SELECT code_gender, COUNT(*) as count,
                AVG(amt_income_total) as avg_income
            FROM client_data
            GROUP BY code_gender
        """)
        fig = px.bar(gender_dist, x='code_gender', y='count',
                    title='Gender Distribution',
                    labels={'code_gender': 'Gender', 'count': 'Number of Clients'})
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Age distribution
        age_dist = execute_query(engine, """
            SELECT 
                CASE 
                    WHEN DAYS_BIRTH/(-365) < 25 THEN '18-25'
                    WHEN DAYS_BIRTH/(-365) < 35 THEN '26-35'
                    WHEN DAYS_BIRTH/(-365) < 45 THEN '36-45'
                    WHEN DAYS_BIRTH/(-365) < 55 THEN '46-55'
                    ELSE '55+'
                END as age_group,
                COUNT(*) as count
            FROM client_data
            GROUP BY age_group
            ORDER BY age_group
        """)
        fig = px.bar(age_dist, x='age_group', y='count',
                    title='Age Distribution',
                    labels={'age_group': 'Age Group', 'count': 'Number of Clients'})
        st.plotly_chart(fig, use_container_width=True)
    
    # Family status and credit
    st.subheader("Family Status Impact on Credit")
    family_credit = execute_query(engine, """
        SELECT 
            c.name_family_status,
            cr.status,
            COUNT(*) as count
        FROM client_data c
        JOIN credit_record cr ON c.id = cr.id
        GROUP BY c.name_family_status, cr.status
        ORDER BY count DESC
    """)
    fig = px.sunburst(family_credit, 
                    path=['name_family_status', 'status'],
                    values='count',
                    title='Family Status and Credit Status Distribution')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Income Analysis":
    st.title("💰 Income Analysis")
    
    # Income distribution
    st.subheader("Income Distribution by Type")
    
    fig = px.box(execute_query(engine, """
        SELECT name_income_type, amt_income_total
        FROM client_data
    """), x='name_income_type', y='amt_income_total',
                title='Income Distribution by Type')
    st.plotly_chart(fig, use_container_width=True)
    
    # Income vs Credit Status
    st.subheader("Income Level Impact on Credit Status")
    income_credit = execute_query(engine, """
        SELECT 
            CASE 
                WHEN c.amt_income_total < 50000 THEN 'Low Income'
                WHEN c.amt_income_total < 100000 THEN 'Middle Income'
                WHEN c.amt_income_total < 200000 THEN 'High Income'
                ELSE 'Very High Income'
            END as income_category,
            cr.status,
            COUNT(*) as count
        FROM client_data c
        JOIN credit_record cr ON c.id = cr.id
        GROUP BY income_category, cr.status
        ORDER BY count DESC
    """)
    
    fig = px.treemap(income_credit,
                    path=['income_category', 'status'],
                    values='count',
                    title='Income Level and Credit Status Distribution')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Credit Status":
    st.title("📈 Credit Status Analysis")
    
    # Status trends over time
    st.subheader("Credit Status Trends")
    status_trend = execute_query(engine, """
        SELECT 
            months_balance,
            status,
            COUNT(*) as count
        FROM credit_record
        GROUP BY months_balance, status
        ORDER BY months_balance
    """)
    
    fig = px.line(status_trend, x='months_balance', y='count', color='status',
                title='Credit Status Trends Over Time')
    st.plotly_chart(fig, use_container_width=True)
    
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
    
    # Create transition matrix heatmap
    pivot_transitions = transitions.pivot(index='current_status', 
                                    columns='next_status', 
                                    values='transitions').fillna(0)
    
    fig = px.imshow(pivot_transitions,
                    title='Credit Status Transition Matrix',
                    labels=dict(x='Next Status', y='Current Status', color='Number of Transitions'))
    st.plotly_chart(fig, use_container_width=True)

elif page == "Educational Impact":
    st.title("🎓 Educational Impact Analysis")
    
    # Education type distribution
    st.subheader("Education Type Distribution")
    edu_dist = execute_query(engine, """
        SELECT 
            name_education_type,
            COUNT(*) as count,
            AVG(amt_income_total) as avg_income
        FROM client_data
        GROUP BY name_education_type
        ORDER BY count DESC
    """)
    
    fig = px.bar(edu_dist,
                x='name_education_type',
                y=['count', 'avg_income'],
                title='Education Type Distribution and Average Income',
                barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    # Education and credit status
    st.subheader("Education Impact on Credit Status")
    edu_credit = execute_query(engine, """
        SELECT 
            c.name_education_type,
            cr.status,
            COUNT(*) as count
        FROM client_data c
        JOIN credit_record cr ON c.id = cr.id
        GROUP BY c.name_education_type, cr.status
        ORDER BY count DESC
    """)
    
    fig = px.sunburst(edu_credit,
                    path=['name_education_type', 'status'],
                    values='count',
                    title='Education Type and Credit Status Distribution')
    st.plotly_chart(fig, use_container_width=True)

elif page == "Custom Analysis":
    st.title("🔍 Custom Analysis")
    
    # Allow users to select variables for analysis
    st.subheader("Create Custom Analysis")
    
    # Select variables
    numeric_columns = ['amt_income_total', 'cnt_children', 'days_employed', 'cnt_fam_members']
    categorical_columns = ['code_gender', 'name_education_type', 'name_family_status', 'name_income_type']
    
    analysis_type = st.selectbox("Select Analysis Type",
                            ["Correlation", "Distribution", "Cross-tabulation"])
    
    if analysis_type == "Correlation":
        var1 = st.selectbox("Select first variable", numeric_columns)
        var2 = st.selectbox("Select second variable", numeric_columns)
        
        correlation_data = execute_query(engine, f"""
            SELECT {var1}, {var2}
            FROM client_data
            WHERE {var1} IS NOT NULL AND {var2} IS NOT NULL
        """)
        
        fig = px.scatter(correlation_data, x=var1, y=var2,
                        title=f'Correlation between {var1} and {var2}')
        st.plotly_chart(fig, use_container_width=True)
        
    elif analysis_type == "Distribution":
        var = st.selectbox("Select variable", numeric_columns + categorical_columns)
        
        if var in numeric_columns:
            dist_data = execute_query(engine, f"""
                SELECT {var}
                FROM client_data
                WHERE {var} IS NOT NULL
            """)
            fig = px.histogram(dist_data, x=var,
                            title=f'Distribution of {var}')
        else:
            dist_data = execute_query(engine, f"""
                SELECT {var}, COUNT(*) as count
                FROM client_data
                WHERE {var} IS NOT NULL
                GROUP BY {var}
                ORDER BY count DESC
            """)
            fig = px.bar(dist_data, x=var, y='count',
                        title=f'Distribution of {var}')
        
        st.plotly_chart(fig, use_container_width=True)
        
    else:  # Cross-tabulation
        var1 = st.selectbox("Select first variable", categorical_columns)
        var2 = st.selectbox("Select second variable", categorical_columns)
        
        crosstab_data = execute_query(engine, f"""
            SELECT {var1}, {var2}, COUNT(*) as count
            FROM client_data
            WHERE {var1} IS NOT NULL AND {var2} IS NOT NULL
            GROUP BY {var1}, {var2}
            ORDER BY count DESC
        """)
        
        pivot_data = crosstab_data.pivot(index=var1, columns=var2, values='count').fillna(0)
        fig = px.imshow(pivot_data,
                        title=f'Cross-tabulation of {var1} vs {var2}',
                        labels=dict(x=var2, y=var1, color='Count'))
        st.plotly_chart(fig, use_container_width=True)
