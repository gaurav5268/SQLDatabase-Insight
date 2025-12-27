import sqlite3
import pandas as pd
import os
import sys

DB_NAME = "database.db"
DATA_FOLDER = "data"
SCHEMA_FILE = os.path.join(DATA_FOLDER, "schema.sql")

IMPORT_ORDER = ["employee.csv","department.csv","dept_emp.csv","title.csv","salary.csv"]


def log(msg):
    print(f"\n🔹 {msg}")


def exit_error(msg):
    print(f"\n ERROR: {msg}")
    sys.exit(1)



if not os.path.exists(DATA_FOLDER):
    exit_error(f"Data folder not found: {DATA_FOLDER}")

if not os.path.exists(SCHEMA_FILE):
    exit_error(f"Schema file missing: {SCHEMA_FILE}")



if os.path.exists(DB_NAME):
    os.remove(DB_NAME)
    print(f"\n Old database removed → {DB_NAME}")

print(f"\n Creating new SQLite database → {DB_NAME}")

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")
print("Foreign key enforcement enabled")


log("Creating tables from schema.sql ...")

with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
    schema_sql = f.read()

try:
    cursor.executescript(schema_sql)
    print("✔ Schema created successfully")
except Exception as e:
    exit_error(f"Schema execution failed → {e}")


for file in IMPORT_ORDER:

    path = os.path.join(DATA_FOLDER, file)

    if not os.path.exists(path):
        exit_error(f"CSV file missing: {file}")

    table = file.replace(".csv", "")

    log(f"Importing table → {table}")

    df = pd.read_csv(path, sep=None, engine="python")

    df.columns = (
        df.columns
        .str.replace('"', '')
        .str.replace("'", '')
        .str.replace(";", '')
        .str.replace("\ufeff", '')  # remove BOM
        .str.strip()
        .str.lower()
    )

    print("Detected columns:", list(df.columns))

    try:
        df.to_sql(table, conn, if_exists="append", index=False)
        print(f"✔ Loaded {len(df)} rows into {table}")
    except Exception as e:
        exit_error(f"Insert failed for {table} → {e}")

conn.commit()
conn.close()

print("\n🎯 SQLite database built successfully!")
print(f"📦 Output file → {DB_NAME}")
