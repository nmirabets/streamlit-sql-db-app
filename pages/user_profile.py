import streamlit as st
import auth
import auth_ui

# Page configuration
st.set_page_config(
    page_title="User Profile",
    page_icon="👤",
    layout="wide"
)

# Check authentication
auth.require_authentication()

# Show authentication status and navigation
auth_ui.show_auth_sidebar()
auth_ui.show_navigation()

# Show user profile
auth_ui.show_user_profile()