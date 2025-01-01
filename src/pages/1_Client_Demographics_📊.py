# pages/client_demographics.py

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
st.title("👥 Client Demographics Analysis")

# Create two columns for Gender and Age Distribution
col1, col2 = st.columns(2)

with col1:
    # Gender distribution
    st.subheader("Gender Distribution")
    gender_dist = execute_query(engine, """
        SELECT code_gender, COUNT(*) as count,
        AVG(amt_income_total) as avg_income
        FROM client_data
        GROUP BY code_gender
    """)
    
    if not gender_dist.empty:
        # Map gender codes to labels (assuming 'F', 'M', 'X')
        gender_mapping = {'F': 'Female', 'M': 'Male', 'X': 'Other'}
        gender_dist['gender_label'] = gender_dist['code_gender'].map(gender_mapping)
        
        fig = px.bar(
            gender_dist, 
            x='gender_label', 
            y='count',
            color='gender_label',
            title='Gender Distribution',
            labels={'gender_label': 'Gender', 'count': 'Number of Clients'},
            color_discrete_sequence=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for Gender Distribution.")

with col2:
    # Age distribution
    st.subheader("Age Distribution")
    age_dist = execute_query(engine, """
    SELECT 
        CASE 
            WHEN (DAYS_BIRTH / (-365)) < 25 THEN '18-25'
            WHEN (DAYS_BIRTH / (-365)) < 35 THEN '26-35'
            WHEN (DAYS_BIRTH / (-365)) < 45 THEN '36-45'
            WHEN (DAYS_BIRTH / (-365)) < 55 THEN '46-55'
            ELSE '55+'
        END as age_group,
        COUNT(*) as count
    FROM client_data
    GROUP BY 
        CASE 
            WHEN (DAYS_BIRTH / (-365)) < 25 THEN '18-25'
            WHEN (DAYS_BIRTH / (-365)) < 35 THEN '26-35'
            WHEN (DAYS_BIRTH / (-365)) < 45 THEN '36-45'
            WHEN (DAYS_BIRTH / (-365)) < 55 THEN '46-55'
            ELSE '55+'
        END
    ORDER BY 
        MIN(DAYS_BIRTH / (-365))  -- This will naturally order the age groups
    """)
    
    if not age_dist.empty:
        fig = px.bar(
            age_dist, 
            x='age_group', 
            y='count',
            title='Age Distribution',
            labels={'age_group': 'Age Group', 'count': 'Number of Clients'},
            color='age_group',
            color_discrete_sequence=px.colors.sequential.Plasma
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No data available for Age Distribution.")

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

if not family_credit.empty:
    fig = px.sunburst(
        family_credit,
        path=['name_family_status', 'status'],
        values='count',
        title='Family Status and Credit Status Distribution',
        color='count',
        color_continuous_scale='RdBu'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for Family Status Impact on Credit.")
