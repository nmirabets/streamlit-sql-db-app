import streamlit as st
from functions import run_query, initialize_database
import queries as q
import auth
import auth_ui

st.title("Add Employee")

# Check authentication
auth.require_authentication()

# Show authentication status and navigation
auth_ui.show_auth_sidebar()
auth_ui.show_navigation()

# Initialize database (cached - runs only once per session)
engine = initialize_database(q.DATABASE_SCHEMA)

# Add employee form
with st.form("add_employee_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    department = st.selectbox("Department", ["Engineering", "Marketing", "Sales", "HR"])
    salary = st.number_input("Salary", min_value=0, step=1000)
    hire_date = st.date_input("Hire Date")
    submit_button = st.form_submit_button("Add Employee")

    if submit_button:
        params = {
            'name': name,
            'email': email,
            'department': department,
            'salary': salary,
            'hire_date': hire_date
        }
        print(f"Executing query with params: {params}")
        run_query(engine, q.INSERT_DATA_SQL, params)
        st.success("Employee added successfully!")