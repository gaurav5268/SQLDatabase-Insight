from langchain.prompts import PromptTemplate

SCHEMA = """
Tables and columns in MySQL database `employee`:

1. employee(
    emp_no INT PRIMARY KEY,
    birth_date DATE,
    first_name VARCHAR(14),
    last_name VARCHAR(16),
    gender ENUM('M','F'),
    hire_date DATE
)

2. department(
    dept_no CHAR(4) PRIMARY KEY,
    dept_name VARCHAR(40) UNIQUE
)

3. dept_emp(
    emp_no INT,
    dept_no CHAR(4),
    PRIMARY KEY (emp_no, dept_no),
    FOREIGN KEY (emp_no) REFERENCES employee(emp_no),
    FOREIGN KEY (dept_no) REFERENCES department(dept_no)
)

4. title(
    emp_no INT,
    title VARCHAR(50),
    FOREIGN KEY (emp_no) REFERENCES employee(emp_no)
)

5. salary(
    emp_no INT,
    amount INT,
    FOREIGN KEY (emp_no) REFERENCES employee(emp_no)
)
"""

FEW_SHOTS = """
User: How many employees are there?
Answer:
1. Total number of employees is -
2. SELECT COUNT(*) FROM employee;

User: Show me the first name, last name, and salary of employees earning more than 10000
Answer:
1. Here are the employees earning more than 10000 with their names and salaries -
2. SELECT e.first_name AS Name, e.last_name AS LastName, s.amount AS Salary
     FROM employee AS e
     JOIN salary AS s ON e.emp_no = s.emp_no
     WHERE s.amount > 10000;

User: Which departments do we have?
Answer:
1. The departments available are -
2. SELECT dept_name AS Department FROM department;

User: List the employees working in the 'Finance' department
Answer:
1. Employees working in the Finance department are -
2. SELECT e.first_name AS Name, e.last_name AS LastName
     FROM employee AS e
     JOIN dept_emp AS de ON e.emp_no = de.emp_no
     JOIN department AS d ON de.dept_no = d.dept_no
     WHERE d.dept_name = 'Finance';

User: Show me the distribution of employees by departments in a bar chart
Answer:
1. Employee distribution by departments -
2. SELECT d.dept_name AS Department, COUNT(*) AS EmployeeCount
     FROM department AS d
     JOIN dept_emp AS de ON d.dept_no = de.dept_no
     GROUP BY d.dept_name
     ORDER BY EmployeeCount DESC;

User: Show me number of male and female senior engineers in a bar chart
Answer:
1. Gender distribution of Senior Engineers -
2. SELECT e.gender AS Gender, COUNT(*) AS Count
     FROM employee AS e
     JOIN title AS t ON e.emp_no = t.emp_no
     WHERE t.title = 'Senior Engineer'
     GROUP BY e.gender;
"""

prompt = PromptTemplate(
    input_variables=["question"],
    template=f"""
You are a MySQL assistant. 
You are experienced in MySQL commands. 
Convert natural language into two parts:

1. A short natural language response template.  
   - Example: "Total number of employees is -"  
   - Generate response in users language only.
   - Should not include actual numbers unless query result is available.  
   - Phrase it so we can append SQL result later.  

2. A valid MySQL query.  
   - Use only given tables/columns.  
   - Use explicit JOINs when needed.  
   - Use table aliases for readability (e.g., "Name", "Department", "Salary", "Count")
   - Always give meaningful column names in output using AS (i.e "Name", "Salary"), never raw database column names
   - For chart queries, ensure proper GROUP BY and aggregation functions
   - Return only the SQL query (no markdown, no ```sql).  

Schema:
{SCHEMA}

Examples:
{FEW_SHOTS}

Now, generate answer for:

User: {{question}}
Answer:
"""
)
