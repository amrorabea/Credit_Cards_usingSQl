# pages/educational_impact.py

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
st.title("🎓 Educational Impact Analysis")

# Education type distribution and average income
st.subheader("Education Type Distribution and Average Income")
edu_dist = execute_query(engine, """
    SELECT 
        name_education_type,
        COUNT(*) as count,
        AVG(amt_income_total) as avg_income
    FROM client_data
    GROUP BY name_education_type
    ORDER BY count DESC
""")

if not edu_dist.empty:
    # Create grouped bar chart for count and average income
    fig = px.bar(
        edu_dist,
        x='name_education_type',
        y=['count', 'avg_income'],
        title='Education Type Distribution and Average Income',
        labels={
            'value': 'Count / Average Income',
            'name_education_type': 'Education Type'
        },
        barmode='group',
        color_discrete_sequence=['#636EFA', '#EF553B']
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for Education Type Distribution and Average Income.")

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

if not edu_credit.empty:
    fig = px.sunburst(
        edu_credit,
        path=['name_education_type', 'status'],
        values='count',
        title='Education Type and Credit Status Distribution',
        color='count',
        color_continuous_scale='RdBu'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for Education Impact on Credit Status.")
