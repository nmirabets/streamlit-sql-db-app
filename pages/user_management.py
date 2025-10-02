import streamlit as st
import auth
import auth_ui

# Page configuration
st.set_page_config(
    page_title="User Management",
    page_icon="👥",
    layout="wide"
)

# Check authentication and require admin role
auth.require_role('admin')

# Show authentication status and navigation
auth_ui.show_auth_sidebar()
auth_ui.show_navigation()

# Show user management interface
auth_ui.show_user_management()