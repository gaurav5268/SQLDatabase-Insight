# Natural Language Database Insights Project (Text-to-SQL + CSV Dataset)

A database insights and analytics project that allows users to explore and analyze structured database records using natural-language queries.

The system is designed to work with relational databases. SQLite is used only as a lightweight deployment database for portability and easy execution.

The application is later integrated with a Streamlit + LLM powered pipeline to automatically generate SQL queries, insights, tables, and visual charts from user queries.

The project includes:

✔ Natural Language → SQL Query Generation  
✔ Schema-Aware Database Understanding  
✔ Relational Dataset with Foreign-Key Mapping  
✔ Clean CSV-Based Data Import Pipeline  
✔ Automatic Database Build & Rebuild Support  
✔ Backend Dataset for Insight & Analytics System  

---

## Problem Statement

Database exploration normally requires writing SQL queries manually, understanding table relationships, validating foreign-key constraints, and handling structured dataset imports. For learners, analysts, and non-technical users this becomes complex and time-consuming.

This project solves that by:

- Preparing a clean and structured relational dataset  
- Loading data in dependency-safe order  
- Preserving referential integrity  
- Enabling natural-language driven database insights  

The database serves as a backend for:

🟢 SQL learning and practice  
🟢 Data analytics and reporting  
🟢 Natural-language query understanding  

---

## Dataset

The dataset is stored in CSV format and imported into the database.

Tables included:

employee — Employee personal and demographic details  
department — Department master data  
dept_emp — Employee–Department mapping  
title — Employee role and designation  
salary — Salary records  

The import process maintains relational consistency and foreign-key safety.

---

## Database Processing Pipeline

Step 1 — Create tables from schema  
Step 2 — Load data from CSV files  
Step 3 — Normalize and clean column headers  
Step 4 — Insert data in dependency-safe order  
Step 5 — Validate relational constraints  
Step 6 — Finalize database for analytics use  

This ensures:

✔ No partial or corrupt imports  
✔ No broken relationships  
✔ Consistent and reproducible dataset  

---

## Business & Learning Objectives

This project is designed for:

✔ Understanding relational database concepts  
✔ Practicing SQL and analytical queries  
✔ Hands-on data engineering workflow  
✔ Backend dataset for insight applications  
✔ Natural-language database exploration  

Example natural-language queries supported:

- Show employees working in Finance department  
- List salaries of Senior Engineers  
- Department-wise employee distribution  
- Generate chart of employees by title  

The system converts user queries to SQL and fetches insights automatically.

---

## Tech Stack

Languages — Python  
Database Runtime — SQLite (deployment convenience only; design is database-agnostic)  
Libraries — Pandas  
Data Source — CSV + Schema SQL  
Application Usage — Text-to-SQL Analytics Backend  

---

## Project Architecture

data/  
 ├── schema.sql  
 ├── employee.csv  
 ├── department.csv  
 ├── dept_emp.csv  
 ├── title.csv  
 └── salary.csv  

.env  
app.py  
main.py  
prompts.py  

build_database.py  
database.db  

requirements.txt  
README.md  

---

## Installation & Setup

1) Install dependencies

pip install pandas

2) Run the database build script

python build_database.py

A clean database is generated:

database.db

Existing database is automatically deleted and rebuilt to ensure consistency and reproducibility.

---

## Key Highlights

✔ Designed for database-centric learning and insights  
✔ Clean relational dataset for analytics projects  
✔ Automatic rebuild mechanism  
✔ Suitable for LLM + Streamlit-based systems  
✔ Lightweight runtime storage backend  

---

Gaurav Chauhan
