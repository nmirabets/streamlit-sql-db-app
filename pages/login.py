import streamlit as st
import auth
import auth_ui

# Page configuration
st.set_page_config(
    page_title="Login - Employee Dashboard",
    page_icon="🔐",
    layout="centered"
)

# Check if user is already authenticated
if auth.is_authenticated():
    st.success("You are already logged in!")
    st.info("Click below to go to the dashboard")
    if st.button("Go to Dashboard", type="primary"):
        st.switch_page("pages/dashboard.py")
    st.stop()

# Show login and registration tabs
tab1, tab2 = st.tabs(["Login", "Register"])

with tab1:
    auth_ui.show_login_form()

with tab2:
    auth_ui.show_registration_form()

# Instructions
st.markdown("---")
st.markdown("### 📋 Instructions")
st.markdown("""
- **New users**: Use the Register tab to create an account
- **Existing users**: Use the Login tab to access your account
- **Default roles**: 
  - `user`: Basic access to dashboard and add employees
  - `manager`: Access to user profile and basic features
  - `admin`: Full access including user management
""")