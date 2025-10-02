import streamlit as st
import pandas as pd
import auth

def show_login_form():
    """Display login form."""
    st.title("🔐 Login")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Login")
        
        if submit_button:
            if username and password:
                user_data = auth.authenticate_user(username, password)
                if user_data:
                    auth.login_user(user_data)
                    st.success(f"Welcome back, {user_data['username']}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
            else:
                st.error("Please enter both username and password")

def show_registration_form():
    """Display registration form."""
    st.title("📝 Register")
    
    with st.form("registration_form"):
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")
        role = st.selectbox("Role", ["user", "manager", "admin"])
        submit_button = st.form_submit_button("Register")
        
        if submit_button:
            # Validation
            if not username or not email or not password:
                st.error("Please fill in all fields")
                return
            
            if not auth.validate_username(username):
                st.error("Username must be 3-50 characters and contain only letters, numbers, and underscores")
                return
            
            if not auth.validate_email(email):
                st.error("Please enter a valid email address")
                return
            
            if not auth.validate_password(password):
                st.error("Password must be at least 8 characters long")
                return
            
            if password != password_confirm:
                st.error("Passwords do not match")
                return
            
            # Create user
            if auth.create_user(username, email, password, role):
                st.success("Registration successful! You can now log in.")
                st.balloons()
            else:
                st.error("Registration failed. Username or email might already exist.")

def show_user_profile():
    """Display current user profile."""
    if not auth.is_authenticated():
        st.error("Please log in to view your profile")
        return
    
    user = auth.get_current_user()
    
    st.title(f"👤 Welcome, {user['username']}!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("**User Information**")
        st.write(f"**Username:** {user['username']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Role:** {user['role'].title()}")
        st.write(f"**Member since:** {user['created_at'].strftime('%B %d, %Y')}")
        
        if user.get('last_login'):
            st.write(f"**Last login:** {user['last_login'].strftime('%B %d, %Y at %I:%M %p')}")
    
    with col2:
        st.info("**Session Information**")
        login_time = st.session_state.get('login_time')
        if login_time:
            st.write(f"**Current session started:** {login_time.strftime('%I:%M %p')}")
        
        if st.button("🚪 Logout", type="primary"):
            auth.logout_user()
            st.success("Logged out successfully!")
            st.rerun()

def show_user_management():
    """Display user management interface (admin only)."""
    auth.require_role('admin')
    
    st.title("👥 User Management")
    
    # Get all users
    users_df = auth.get_all_users()
    
    if len(users_df) > 0:
        st.subheader("All Users")
        
        # Format the dataframe for display
        display_df = users_df.copy()
        display_df['created_at'] = pd.to_datetime(display_df['created_at']).dt.strftime('%Y-%m-%d')
        display_df['last_login'] = pd.to_datetime(display_df['last_login']).dt.strftime('%Y-%m-%d %H:%M')
        
        st.dataframe(
            display_df.rename(columns={
                'id': 'ID',
                'username': 'Username',
                'email': 'Email',
                'role': 'Role',
                'created_at': 'Created',
                'last_login': 'Last Login'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # User statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Users", len(users_df))
        
        with col2:
            admin_count = len(users_df[users_df['role'] == 'admin'])
            st.metric("Admins", admin_count)
        
        with col3:
            manager_count = len(users_df[users_df['role'] == 'manager'])
            st.metric("Managers", manager_count)
    else:
        st.info("No users found")

def show_auth_sidebar():
    """Display authentication status in sidebar."""
    with st.sidebar:
        if auth.is_authenticated():
            user = auth.get_current_user()
            st.success(f"✅ Logged in as: **{user['username']}**")
            st.write(f"Role: {user['role'].title()}")
            
            if st.button("🚪 Logout", key="sidebar_logout"):
                auth.logout_user()
                st.rerun()
        else:
            st.error("❌ Not logged in")

def show_navigation():
    """Display navigation menu based on user role."""
    if not auth.is_authenticated():
        return
    
    user = auth.get_current_user()
    
    st.sidebar.title("🧭 Navigation")
    
    # Basic navigation for all users
    st.sidebar.page_link("pages/dashboard.py", label="📊 Dashboard", icon="📊")
    st.sidebar.page_link("pages/add_employee.py", label="👤 Add Employee", icon="👤")
    
    # Manager and Admin navigation
    if auth.has_role('manager'):
        st.sidebar.page_link("pages/user_profile.py", label="👤 Profile", icon="👤")
    
    # Admin only navigation
    if auth.has_role('admin'):
        st.sidebar.page_link("pages/user_management.py", label="👥 User Management", icon="👥")
        st.sidebar.page_link("pages/register_user.py", label="📝 Register User", icon="📝")
    
    # Login page link for unauthenticated users
    st.sidebar.page_link("pages/login.py", label="🔐 Login", icon="🔐")