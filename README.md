# 🚀 Neon Database + Streamlit Tutorial

**Learn to build data-driven web applications using PostgreSQL and Python!**

This tutorial teaches bootcamp students how to:
- Set up a free PostgreSQL database with [Neon](https://neon.com/)
- Connect to the database using Python
- Create tables and insert data with SQL
- Build a simple Streamlit web application to display data

## 📋 Prerequisites

- Basic Python knowledge
- Understanding of SQL fundamentals
- Python 3.7+ installed on your computer

## 🎯 Learning Objectives

By the end of this tutorial, you'll be able to:
- ✅ Create and configure a Neon PostgreSQL database
- ✅ Connect to a database using Python and SQLAlchemy
- ✅ Execute SQL commands to create tables and insert data
- ✅ Build a Streamlit web app that displays data in tables and charts
- ✅ Deploy your database-driven application

## 📚 Tutorial Structure

### Phase 1: Database Setup & Learning (Jupyter Notebook)
1. **Setup Neon Account** - Create your free database
2. **Complete the Notebook** - Learn database basics with `Neon_Database_Guide.ipynb`
3. **Practice SQL** - Run queries and understand the data

### Phase 2: Web Application Development (Streamlit)
1. **Create Streamlit App** - Build a data dashboard
2. **Add Visualizations** - Display data with tables and charts
3. **Test Your Application** - Run and refine your app

---

## 🗄️ Phase 1: Setting Up Your Neon Database

### Step 1: Create a Neon Account

1. **Visit [Neon.com](https://neon.com/)**
2. **Click "Sign Up"** - It's free!
3. **Choose your signup method:**
   - GitHub account (recommended for developers)
   - Google account
   - Email and password

### Step 2: Create Your First Database

1. **After signing up**, you'll be taken to the Neon Console
2. **Click "Create Project"** 
3. **Choose your settings:**
   - **Project Name**: `streamlit-tutorial` (or any name you prefer)
   - **Database Name**: `neondb` (default is fine)
   - **Region**: Choose the closest to your location
4. **Click "Create Project"**

### Step 3: Get Your Database Connection String

1. **In your Neon Console**, find your project
2. **Go to the "Dashboard" tab**
3. **Find the "Connection Details" section**
4. **Copy the connection string** - it looks like:
   ```
   postgresql://username:password@host.neon.tech/database_name?sslmode=require
   ```
5. **Keep this safe** - you'll need it in the next steps!

### Step 4: Set Up Your Environment

1. **Clone or download this repository**
2. **Navigate to the project folder**
3. **Create a `.env` file** in the project root:
   ```bash
   touch .env
   ```
4. **Add your database URL** to the `.env` file:
   ```
   DATABASE_URL=your_connection_string_here
   ```
   ⚠️ **Important**: Replace `your_connection_string_here` with the actual connection string from Neon!

### Step 5: Install Required Packages

```bash
pip install sqlalchemy pandas python-dotenv matplotlib seaborn jupyter
```

### Step 6: Complete the Jupyter Notebook Tutorial

1. **Open the notebook:**
   ```bash
   jupyter notebook Neon_Database_Guide.ipynb
   ```
2. **Run through all cells** - this will:
   - Connect to your database
   - Create an `employees` table
   - Insert sample data
   - Run queries to explore the data
3. **Experiment with the SQL queries** - try modifying them!
4. **Understand the data structure** - you'll use this in your Streamlit app

---

## 🌐 Phase 2: Building Your Streamlit Application

Now that you understand the database, let's build a web application!

### Step 1: Install Streamlit

```bash
pip install streamlit
```

### Step 2: Create Your Streamlit App

Create a new file called `streamlit_app.py` and build an application that:

**Required Features:**
- 📊 **Data Table**: Display all employees in a table
- 📈 **Salary Chart**: Show average salary by department
- 🎨 **Clean Design**: Use Streamlit's built-in styling

**Suggested Structure:**
```python
# Your app should include:
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# 1. Page configuration
# 2. Database connection
# 3. Data loading functions
# 4. Main app layout with title
# 5. Display data table
# 6. Create and display charts
```

### Step 3: Features to Implement

**🔧 Core Features (Required):**
- Connect to your Neon database
- Display employee data in a table
- Show a chart of average salaries by department
- Add a title and description

**🌟 Bonus Features (Optional):**
- Filter employees by department
- Add more chart types (bar chart, pie chart)
- Show employee count by department
- Add form to insert new employees

### Step 4: Run Your Application

```bash
streamlit run streamlit_app.py
```

Your app will open in your browser at `http://localhost:8501`

### Step 5: Test and Iterate

- **Test all features** - make sure data loads correctly
- **Check your charts** - verify they display the right information
- **Improve the design** - add colors, better layouts
- **Add error handling** - what happens if the database is unavailable?

---

## 📝 What You Should Build

Your final Streamlit application should include:

### 📊 **Data Table Section**
- Display all employees with columns: Name, Email, Department, Salary, Hire Date
- Make it sortable and searchable (Streamlit does this automatically!)

### 📈 **Visualization Section** 
- **Bar Chart**: Average salary by department
- **Optional**: Employee count by department
- **Optional**: Salary distribution histogram

### 🎨 **User Interface**
- Clean, professional layout
- Clear headings and descriptions
- Responsive design that works on different screen sizes

---

## 🔧 Technical Requirements

### File Structure
```
streamlit-sql-db-app/
├── README.md                 # This tutorial
├── Neon_Database_Guide.ipynb # Learning notebook
├── streamlit_app.py          # Your web application
├── .env                      # Database credentials (create this)
├── .env.sample              # Example environment file
└── requirements.txt         # Python dependencies (optional)
```

### Environment Variables
Create a `.env` file with:
```
DATABASE_URL=postgresql://username:password@host.neon.tech/database_name?sslmode=require
```

### Python Packages Needed
```
streamlit
sqlalchemy
pandas
python-dotenv
matplotlib
seaborn
```

---

## 🚨 Troubleshooting

### Database Connection Issues
- ✅ **Check your `.env` file** - make sure the DATABASE_URL is correct
- ✅ **Verify your Neon project** - ensure it's not paused
- ✅ **Test connection** - run the notebook first to verify connectivity

### Streamlit Issues
- ✅ **Port conflicts** - try `streamlit run streamlit_app.py --server.port 8502`
- ✅ **Package issues** - reinstall with `pip install --upgrade streamlit`
- ✅ **Cache problems** - clear cache with `streamlit cache clear`

### Data Not Showing
- ✅ **Run the notebook first** - make sure data exists in your database
- ✅ **Check SQL queries** - test them in the notebook
- ✅ **Debug with print statements** - add `st.write()` to see data

---

## 🎉 Completion Checklist

**Phase 1: Database Setup**
- [ ] Created Neon account successfully
- [ ] Set up database project
- [ ] Obtained connection string
- [ ] Created `.env` file with credentials
- [ ] Completed Jupyter notebook tutorial
- [ ] Successfully connected to database
- [ ] Ran SQL queries and saw results

**Phase 2: Streamlit Application**
- [ ] Created `streamlit_app.py` file
- [ ] Connected to database in Streamlit
- [ ] Displayed employee data in a table
- [ ] Created salary chart by department
- [ ] Added proper titles and descriptions
- [ ] Tested application runs without errors
- [ ] **Bonus**: Added additional features or styling

**🏆 Advanced Challenges (Optional)**
- [ ] Added form to insert new employees
- [ ] Implemented department filtering
- [ ] Created multiple chart types
- [ ] Added data validation
- [ ] Styled the application with custom CSS
- [ ] Deployed the application online

---

## 🌟 What's Next?

After completing this tutorial, you'll have built a real database-driven web application! Here are some next steps:

- **Add authentication** - let users log in
- **Deploy your app** - share it with the world using Streamlit Cloud
- **Connect to APIs** - fetch real-time data
- **Learn more databases** - explore MongoDB, Redis, etc.
- **Build bigger projects** - create full-stack applications

**Congratulations on building your first data-driven web application! 🎊** 