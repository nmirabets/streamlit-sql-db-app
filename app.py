import streamlit as st
import backend.auth

# Page configuration
st.set_page_config(
    page_title="Employee Management System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main app entry point
st.title("🏢 Employee Management System")

# Check if user is authenticated
if not backend.auth.is_authenticated():
    st.info("Welcome to the Employee Management System!")
    st.markdown("### 🔐 Please log in to continue")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Go to Login", type="primary", use_container_width=True):
            st.switch_page("pages/login.py")
else:
    # User is authenticated, show dashboard
    st.switch_page("pages/dashboard.py")