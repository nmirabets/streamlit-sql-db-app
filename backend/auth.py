import bcrypt
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import text
import backend.functions as f
import backend.queries as q

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_user(username: str, email: str, password: str, role: str = 'user') -> bool:
    """Create a new user in the database."""
    try:
        engine = f.get_initialized_db()
        if engine is None:
            return False
        
        password_hash = hash_password(password)
        
        with engine.connect() as connection:
            connection.execute(
                text(q.CREATE_USER_SQL),
                {
                    'username': username,
                    'email': email,
                    'password_hash': password_hash,
                    'role': role
                }
            )
            connection.commit()
        return True
    except Exception as e:
        st.error(f"Error creating user: {e}")
        return False

def authenticate_user(username: str, password: str) -> dict:
    """Authenticate a user and return user data if successful."""
    try:
        engine = f.get_initialized_db()
        if engine is None:
            return None
        
        with engine.connect() as connection:
            result = connection.execute(
                text(q.GET_USER_SQL),
                {'username': username}
            )
            user_data = result.fetchone()
            
            if user_data and verify_password(password, user_data.password_hash):
                # Update last login
                connection.execute(
                    text(q.UPDATE_LAST_LOGIN_SQL),
                    {'user_id': user_data.id}
                )
                connection.commit()
                
                return {
                    'id': user_data.id,
                    'username': user_data.username,
                    'email': user_data.email,
                    'role': user_data.role,
                    'created_at': user_data.created_at,
                    'last_login': datetime.now()
                }
        return None
    except Exception as e:
        st.error(f"Authentication error: {e}")
        return None

def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return st.session_state.get('authenticated', False)

def get_current_user() -> dict:
    """Get current user data from session state."""
    return st.session_state.get('user', {})

def login_user(user_data: dict):
    """Log in a user by setting session state."""
    st.session_state['authenticated'] = True
    st.session_state['user'] = user_data
    st.session_state['login_time'] = datetime.now()

def logout_user():
    """Log out the current user."""
    st.session_state['authenticated'] = False
    st.session_state['user'] = {}
    if 'login_time' in st.session_state:
        del st.session_state['login_time']

def check_session_timeout(timeout_minutes: int = 30) -> bool:
    """Check if user session has timed out."""
    if not is_authenticated():
        return True
    
    login_time = st.session_state.get('login_time')
    if login_time and datetime.now() - login_time > timedelta(minutes=timeout_minutes):
        logout_user()
        return True
    return False

def require_authentication():
    """Decorator-like function to require authentication for a page."""
    if check_session_timeout():
        st.error("Session timed out. Please log in again.")
        st.stop()
    
    if not is_authenticated():
        st.error("Please log in to access this page.")
        st.stop()

def has_role(required_role: str) -> bool:
    """Check if current user has the required role."""
    if not is_authenticated():
        return False
    
    user = get_current_user()
    user_role = user.get('role', 'user')
    
    # Role hierarchy: admin > manager > user
    role_hierarchy = {'admin': 3, 'manager': 2, 'user': 1}
    
    return role_hierarchy.get(user_role, 0) >= role_hierarchy.get(required_role, 0)

def require_role(required_role: str):
    """Require a specific role to access content."""
    require_authentication()
    
    if not has_role(required_role):
        st.error(f"Access denied. {required_role.title()} role required.")
        st.stop()

def get_all_users() -> pd.DataFrame:
    """Get all users from the database (admin only)."""
    try:
        engine = f.get_initialized_db()
        if engine is None:
            return pd.DataFrame()
        
        return pd.read_sql_query(q.GET_ALL_USERS_SQL, engine)
    except Exception as e:
        st.error(f"Error fetching users: {e}")
        return pd.DataFrame()

def validate_username(username: str) -> bool:
    """Validate username format."""
    if not username or len(username) < 3 or len(username) > 50:
        return False
    return username.isalnum() or '_' in username

def validate_email(email: str) -> bool:
    """Basic email validation."""
    return '@' in email and '.' in email.split('@')[1]

def validate_password(password: str) -> bool:
    """Validate password strength."""
    return len(password) >= 8