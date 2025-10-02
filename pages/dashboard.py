import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import functions as f
import queries as q
import auth
import auth_ui

# Page configuration
st.set_page_config(
    page_title="Employee Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Check authentication
if not auth.is_authenticated():
    st.error("🔐 Please log in to access the dashboard")
    st.info("Click below to go to the login page")
    if st.button("Go to Login", type="primary"):
        st.switch_page("pages/login.py")
    st.stop()

# Show authentication status and navigation
auth_ui.show_auth_sidebar()
auth_ui.show_navigation()

# Initialize database (cached - runs only once per session)
engine = f.initialize_database(q.DATABASE_SCHEMA)

# Dashboard Header
st.title("👥 Employee Dashboard")
st.markdown("---")

# Check if we have data
try:
    total_employees_df = pd.read_sql_query(q.TOTAL_EMPLOYEES_SQL, engine)
    total_employees = total_employees_df['total_employees'].iloc[0]
    
    if total_employees == 0:
        st.warning("No employee data found. Please add some employees first!")
        st.stop()
        
except Exception as e:
    st.error(f"Error connecting to database: {e}")
    st.stop()

# Fetch all data for dashboard
avg_salary_df = pd.read_sql_query(q.AVERAGE_SALARY_SQL, engine)
dept_df = pd.read_sql_query(q.EMPLOYEES_PER_DEPARTMENT_SQL, engine)
hire_dates_df = pd.read_sql_query(q.HIRE_DATES_TIMELINE_SQL, engine)
recent_hires_df = pd.read_sql_query(q.RECENT_HIRES_SQL, engine)
all_employees_df = pd.read_sql_query(q.SELECT_ALL_DATA_SQL, engine)

# Top Row - Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1.container(border=True):
    st.metric(
        label="Total Employees",
        value=total_employees,
        delta=None
    )

with col2.container(border=True):
    avg_salary = avg_salary_df['avg_salary'].iloc[0] if len(avg_salary_df) > 0 else 0
    st.metric(
        label="Average Salary",
        value=f"${avg_salary:,.2f}",
        delta=None
    )

with col3.container(border=True):
    total_departments = len(dept_df)
    st.metric(
        label="Departments",
        value=total_departments,
        delta=None
    )

with col4.container(border=True):
    if len(recent_hires_df) > 0:
        latest_hire = recent_hires_df['hire_date'].iloc[0]
        st.metric(
            label="Latest Hire",
            value=latest_hire.strftime("%b %Y") if pd.notna(latest_hire) else "N/A",
            delta=None
        )
    else:
        st.metric(label="Latest Hire", value="N/A")

st.markdown("---")

# Second Row - Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Employees per Department")
    if len(dept_df) > 0:
        fig_dept = px.pie(
            dept_df, 
            values='employee_count', 
            names='department',
            title="Distribution by Department",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_dept.update_traces(textposition='inside', textinfo='percent+label')
        fig_dept.update_layout(height=400)
        st.plotly_chart(fig_dept, use_container_width=True)
        
        # Department table
        st.dataframe(
            dept_df.rename(columns={
                'department': 'Department',
                'employee_count': 'Employee Count'
            }),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No department data available")

with col2:
    st.subheader("📈 Hiring Timeline")
    if len(hire_dates_df) > 0:
        fig_timeline = px.bar(
            hire_dates_df,
            x='hire_month',
            y='hires_count',
            title="Hires per Month",
            labels={'hire_month': 'Month', 'hires_count': 'Number of Hires'},
            color='hires_count',
            color_continuous_scale='Blues'
        )
        fig_timeline.update_layout(
            xaxis_title="Month",
            yaxis_title="Number of Hires",
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_timeline, use_container_width=True)
    else:
        st.info("No hiring timeline data available")

st.markdown("---")

# Third Row - Recent Hires and All Employees
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🆕 Recent Hires")
    if len(recent_hires_df) > 0:
        # Format the recent hires for better display
        recent_display = recent_hires_df.copy()
        recent_display['salary'] = recent_display['salary'].apply(lambda x: f"${x:,.2f}")
        recent_display['hire_date'] = pd.to_datetime(recent_display['hire_date']).dt.strftime('%Y-%m-%d')
        
        st.dataframe(
            recent_display.rename(columns={
                'name': 'Name',
                'department': 'Department',
                'hire_date': 'Hire Date',
                'salary': 'Salary'
            }),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No recent hires data available")

with col2:
    st.subheader("👥 All Employees")
    if len(all_employees_df) > 0:
        # Format the salary column for better display
        display_df = all_employees_df.copy()
        display_df['salary'] = display_df['salary'].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "N/A")
        display_df['hire_date'] = pd.to_datetime(display_df['hire_date']).dt.strftime('%Y-%m-%d')
        
        # Hide some columns for cleaner display
        columns_to_show = ['name', 'department', 'salary', 'hire_date', 'email']
        display_columns = {
            'name': 'Name',
            'department': 'Department', 
            'salary': 'Salary',
            'hire_date': 'Hire Date',
            'email': 'Email'
        }
        
        st.dataframe(
            display_df[columns_to_show].rename(columns=display_columns),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No employee data available")

# Footer
st.markdown("---")
st.markdown("*Dashboard last updated: " + pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S") + "*")