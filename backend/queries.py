
DATABASE_SCHEMA = [
    """
    CREATE TABLE IF NOT EXISTS employees (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        department VARCHAR(50),
        salary DECIMAL(10, 2),
        hire_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    """,
    """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        role VARCHAR(20) DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP
    );
    """,
]

INSERT_DATA_SQL = """
    INSERT INTO employees (name, email, department, salary, hire_date) VALUES
    (:name, :email, :department, :salary, :hire_date);
    """

SELECT_ALL_DATA_SQL = "SELECT * FROM employees"

# Dashboard Analytics Queries
TOTAL_EMPLOYEES_SQL = "SELECT COUNT(*) as total_employees FROM employees"

AVERAGE_SALARY_SQL = "SELECT ROUND(AVG(salary), 2) as avg_salary FROM employees"

EMPLOYEES_PER_DEPARTMENT_SQL = """
    SELECT department, COUNT(*) as employee_count 
    FROM employees 
    GROUP BY department 
    ORDER BY employee_count DESC
"""

HIRE_DATES_TIMELINE_SQL = """
    SELECT 
        DATE_TRUNC('month', hire_date) as hire_month,
        COUNT(*) as hires_count
    FROM employees 
    GROUP BY DATE_TRUNC('month', hire_date)
    ORDER BY hire_month
"""

RECENT_HIRES_SQL = """
    SELECT name, department, hire_date, salary
    FROM employees
    ORDER BY hire_date DESC
    LIMIT 10
"""

# Authentication Queries
CREATE_USER_SQL = """
    INSERT INTO users (username, email, password_hash, role) 
    VALUES (:username, :email, :password_hash, :role)
"""

GET_USER_SQL = """
    SELECT id, username, email, password_hash, role, created_at, last_login 
    FROM users 
    WHERE username = :username
"""

UPDATE_LAST_LOGIN_SQL = """
    UPDATE users 
    SET last_login = CURRENT_TIMESTAMP 
    WHERE id = :user_id
"""

GET_ALL_USERS_SQL = """
    SELECT id, username, email, role, created_at, last_login 
    FROM users 
    ORDER BY created_at DESC
"""