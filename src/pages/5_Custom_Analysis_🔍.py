# pages/custom_analysis.py

import streamlit as st
import plotly.express as px
from utils.database import execute_query
from utils.database import get_database_connection
from config import setup_page
import pandas as pd

setup_page()

try:
    engine = get_database_connection()
    st.sidebar.success("📊 Connected to database!")
except Exception as e:
    st.error(f"Error connecting to database: {str(e)}")
    st.stop()
st.title("🔍 Custom Analysis")

# Allow users to select variables for analysis
st.subheader("Create Custom Analysis")

# Define available columns
# Adjust column names based on your database schema
numeric_columns = ['amt_income_total', 'cnt_children', 'days_employed', 'cnt_fam_members']
categorical_columns = ['code_gender', 'name_education_type', 'name_family_status', 'name_income_type']

analysis_type = st.selectbox(
    "Select Analysis Type",
    ["Correlation", "Distribution", "Cross-tabulation"]
)

if analysis_type == "Correlation":
    col1, col2 = st.columns(2)
    with col1:
        var1 = st.selectbox("Select first variable", numeric_columns, key='correlation_var1')
    with col2:
        var2 = st.selectbox("Select second variable", numeric_columns, key='correlation_var2')
    
    if var1 and var2:
        if var1 == var2:
            correlation_data = execute_query(engine, f"""
            SELECT {var1}
            FROM client_data
            WHERE {var1} IS NOT NULL AND {var2} IS NOT NULL
            """)
        else:
            correlation_data = execute_query(engine, f"""
                SELECT {var1}, {var2}
                FROM client_data
                WHERE {var1} IS NOT NULL AND {var2} IS NOT NULL
            """)
        
        if not correlation_data.empty:
            fig = px.scatter(
                correlation_data, 
                x=var1, 
                y=var2,
                trendline='ols',
                title=f'Correlation between {var1.replace("_", " ").title()} and {var2.replace("_", " ").title()}',
                labels={
                    var1: var1.replace('_', ' ').title(), 
                    var2: var2.replace('_', ' ').title()
                },
                opacity=0.7
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for the selected variables.")

elif analysis_type == "Distribution":
    var = st.selectbox("Select variable", numeric_columns + categorical_columns, key='distribution_var')
    
    if var:
        if var in numeric_columns:
            dist_data = execute_query(engine, f"""
                SELECT {var}
                FROM client_data
                WHERE {var} IS NOT NULL
            """)
            if not dist_data.empty:
                fig = px.histogram(
                    dist_data, 
                    x=var,
                    nbins=30,
                    title=f'Distribution of {var.replace("_", " ").title()}',
                    labels={var: var.replace('_', ' ').title(), 'count': 'Frequency'},
                    color_discrete_sequence=['#636EFA']
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available for the selected variable.")
        else:
            dist_data = execute_query(engine, f"""
                SELECT {var}, COUNT(*) as count
                FROM client_data
                WHERE {var} IS NOT NULL
                GROUP BY {var}
                ORDER BY count DESC
            """)
            if not dist_data.empty:
                # Map categorical labels to user-friendly names if necessary
                if var == 'code_gender':
                    dist_data['gender_label'] = dist_data[var].map({'F': 'Female', 'M': 'Male', 'X': 'Other'})
                    var_display = 'gender_label'
                else:
                    var_display = var.replace('_', ' ').title()
                
                fig = px.bar(
                    dist_data, 
                    x=var_display, 
                    y='count',
                    title=f'Distribution of {var.replace("_", " ").title()}',
                    labels={'count': 'Number of Clients', var_display: var.replace('_', ' ').title()},
                    color=var_display,
                    color_discrete_sequence=px.colors.sequential.Viridis
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No data available for the selected variable.")

else:  # Cross-tabulation
    col1, col2 = st.columns(2)
    with col1:
        var1 = st.selectbox("Select first variable", categorical_columns, key='crosstab_var1')
    with col2:
        var2 = st.selectbox("Select second variable", categorical_columns, key='crosstab_var2')
    
    if var1 and var2:
        crosstab_data = execute_query(engine, f"""
            SELECT {var1}, {var2}, COUNT(*) as count
            FROM client_data
            WHERE {var1} IS NOT NULL AND {var2} IS NOT NULL
            GROUP BY {var1}, {var2}
            ORDER BY count DESC
        """)
        
        if not crosstab_data.empty:
            # Convert to pivot table without using pivot directly
            pivot_table = pd.crosstab(
                index=crosstab_data[var1],
                columns=crosstab_data[var2],
                values=crosstab_data['count'],
                aggfunc='sum',
                fill_value=0
            )
            
            # Create heatmap
            fig = px.imshow(
                pivot_table,
                labels=dict(
                    x=var2.replace('_', ' ').title(),
                    y=var1.replace('_', ' ').title(),
                    color='Count'
                ),
                title=f'Cross-tabulation of {var1.replace("_", " ").title()} vs {var2.replace("_", " ").title()}',
                color_continuous_scale='Blues'
            )
            
            # Update layout for better readability
            fig.update_layout(
                xaxis_title=var2.replace('_', ' ').title(),
                yaxis_title=var1.replace('_', ' ').title(),
                xaxis={'side': 'bottom'}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Optionally display the raw numbers
            if st.checkbox("Show raw numbers"):
                st.dataframe(pivot_table)
        else:
            st.warning("No data available for the selected variables.")