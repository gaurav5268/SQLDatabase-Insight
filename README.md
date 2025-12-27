# Natural Language Database Insights Project (SQLite + CSV Dataset)

A database-driven project that creates a fully structured SQLite database from CSV files
and allows users to explore and analyze the database using natural-language queries.

This database is later integrated with a Streamlit + LLM based application
to generate SQL queries, insights, tables, and visual charts automatically.

The project includes:

✔ Automatic SQLite Database Creation  
✔ Schema-Based Table Generation  
✔ Foreign-Key Enforced Relationships  
✔ Clean CSV Import Pipeline  
✔ Transaction-Safe Data Loading  
✔ Automatic Database Overwrite & Rebuild  
✔ Backend Dataset for Natural Language SQL Insights  

---

## Problem Statement

Database analysis often requires:

- Writing SQL queries manually  
- Understanding relational schema  
- Debugging foreign-key relationships  
- Handling data imports safely  

For beginners, analysts, and students — this becomes time-consuming and difficult.

This project solves that problem by:

- Automatically creating database from schema  
- Loading CSV data in dependency-safe order  
- Enforcing referential integrity  
- Providing a clean & reproducible dataset  
- Enabling natural-language query insights  

The database is further used for:

🟢 SQL Learning & Practice  
🟢 Data Analytics & Exploration  
🟢 Natural Language Query → SQL Conversion  

---

## Dataset

The database is created from structured CSV files inside the `data/` folder.

Tables included:

| Table Name | Description |
|----------|-----------|
| employee | Employee personal & demographic details |
| department | Department master data |
| dept_emp | Employee–Department mapping |
| title | Employee role & designation |
| salary | Salary records |

Data is imported in correct dependency order to maintain constraints.

---

## Database Pipeline & Processing

Step 1 — Enable Foreign Key Enforcement  
Step 2 — Execute Schema from `schema.sql`  
Step 3 — Load CSV files in referential order  
Step 4 — Clean and normalize column headers  
Step 5 — Insert records into tables  
Step 6 — Commit and finalize SQLite database  

The script ensures:

✔ No partial imports  
✔ No broken relationships  
✔ No duplicate database state  

---

## Business / Learning Objective

This project is designed for:

✔ SQL & Database Concepts Learning  
✔ Data Engineering Practice  
✔ ETL & Dataset Structuring  
✔ Analytics Project Backend  
✔ Natural Language Insight Systems  

It supports natural-language interactions such as:

- "Show employees working in Finance department"
- "List salaries of Senior Engineers"
- "Department wise employee count"
- "Generate chart of employee distribution"

The system converts queries to SQL and fetches results automatically.

---

## Tech Stack

**Languages**
- Python

**Database**
- SQLite

**Libraries**
- Pandas

**Data Source**
- CSV Files + Schema SQL

**Usage**
- Backend for Text-to-SQL Insights System

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

## Installation & Setup

### 1) Install Dependencies

pip install pandas


---

### 2) Run Database Builder Script

python build_database.py


A fresh SQLite database is generated:

database.db

Existing database is:

✔ deleted  
✔ rebuilt  
✔ reloaded with fresh data  

to maintain clean and reproducible state.

---

## Key Highlights

✔ Structured relational dataset  
✔ Completely automated DB creation  
✔ Overwrite-safe rebuild mechanism  
✔ Suitable for projects & portfolios  
✔ Supports LLM + Streamlit insights app  

---

**Gaurav Chauhan**