import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables (for our database credentials)
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def test_connection(engine):
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Connected to database successfully!")
            print(f"Database version: {version}")  # Show first 50 characters
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Make sure your DATABASE_URL is correct!")
        return False
    
def run_query(engine, query, params=None):
    try:
        with engine.connect() as connection:
            if params:
                connection.execute(text(query), params)
            else:
                connection.execute(text(query))
            connection.commit()
        print(f"✅ Query run successfully!")
    except Exception as e:
        print(f"❌ Error running query: {e}")

@st.cache_resource
def get_database_engine():
    """
    Get cached database engine. This function runs only once per session.
    """
    # 1. Open connection with database
    engine = create_engine(DATABASE_URL)
    
    # 2. Test Connection
    if not test_connection(engine):
        st.error("Failed to connect to database!")
        return None
    
    print("✅ Database engine cached successfully!")
    return engine

@st.cache_resource  
def initialize_database_schema(DATABASE_SCHEMA):
    """
    Initialize database schema only once per session.
    """
    engine = get_database_engine()
    if engine is None:
        return None
        
    # 3. Create schema if it doesn't exist
    for query in DATABASE_SCHEMA:
        # Execute the SQL command
        run_query(engine, query)
    
    print("✅ Database schema initialized!")
    return engine

def initialize_database(DATABASE_SCHEMA):
    """
    Legacy function - now uses cached approach
    """
    return initialize_database_schema(DATABASE_SCHEMA)

def get_db_connection():
    """
    Simple function to get database connection for queries
    """
    return get_database_engine()

# Import the schema here to avoid importing it in every page
try:
    import queries as q
    
    @st.cache_resource
    def get_initialized_db():
        """
        Most efficient way to get database connection.
        Use this function in your pages instead of initialize_database().
        """
        return initialize_database_schema(q.DATABASE_SCHEMA)
        
except ImportError:
    # If queries module is not available, provide a fallback
    def get_initialized_db():
        st.error("Database schema not found!")
        return None
