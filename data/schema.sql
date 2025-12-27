-- CREATE DATABASE IF NOT EXISTS employee;
-- USE employee;

-- SELECT 'CREATING DATABASE STRUCTURE' as 'INFO';

-- DROP TABLE IF EXISTS dept_emp,
--                      dept_manager,
--                      title,
--                      salary, 
--                      employee, 
--                      department;

PRAGMA foreign_keys = ON;

CREATE TABLE employee (
    emp_no INTEGER PRIMARY KEY,
    birth_date TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    gender TEXT CHECK (gender IN ('M','F')) NOT NULL,
    hire_date TEXT NOT NULL
);

CREATE TABLE department (
    dept_no TEXT PRIMARY KEY,
    dept_name TEXT NOT NULL UNIQUE
);

CREATE TABLE dept_emp (
    emp_no INTEGER NOT NULL,
    dept_no TEXT NOT NULL,
    PRIMARY KEY (emp_no, dept_no),
    FOREIGN KEY (emp_no) REFERENCES employee(emp_no) ON DELETE CASCADE,
    FOREIGN KEY (dept_no) REFERENCES department(dept_no) ON DELETE CASCADE
);

CREATE TABLE title (
    emp_no INTEGER NOT NULL,
    title TEXT NOT NULL,
    FOREIGN KEY (emp_no) REFERENCES employee(emp_no) ON DELETE CASCADE
);

CREATE TABLE salary (
    emp_no INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    FOREIGN KEY (emp_no) REFERENCES employee(emp_no) ON DELETE CASCADE
);
