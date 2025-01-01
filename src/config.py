import streamlit as st

# Page configuration
def setup_page():
    st.set_page_config(
        page_title="Credit Analysis Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )