import streamlit as st
import auth
import auth_ui

# Page configuration
st.set_page_config(
    page_title="Register User",
    page_icon="📝",
    layout="centered"
)

# Check authentication and require admin role
auth.require_role('admin')

# Show authentication status and navigation
auth_ui.show_auth_sidebar()
auth_ui.show_navigation()

# Show registration form
auth_ui.show_registration_form()