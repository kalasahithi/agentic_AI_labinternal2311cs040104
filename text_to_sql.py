import os
import sqlite3
from dotenv import load_dotenv
from google import genai

# -----------------------------
# 1. Gemini Client
# -----------------------------
load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "No Gemini API key found. Create a .env file next to this script "
        "with a line like:\nGEMINI_API_KEY=your_key_here"
    )

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.1-flash-lite"


# -----------------------------
# 2. Create Sample Database
# -----------------------------
def create_database():

    conn = sqlite3.connect("company.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            department TEXT,
            salary INTEGER,
            experience INTEGER
        )
    """)

    cursor.execute("DELETE FROM employees")

    employees = [
        (1, "Rahul", "IT", 60000, 3),
        (2, "Priya", "HR", 50000, 2),
        (3, "Arjun", "IT", 75000, 5),
        (4, "Sneha", "Finance", 65000, 4),
        (5, "Kiran", "IT", 90000, 7),
        (6, "Anjali", "HR", 55000, 3)
    ]

    cursor.executemany("""
        INSERT INTO employees
        VALUES (?, ?, ?, ?, ?)
    """, employees)

    conn.commit()

    return conn


# -----------------------------
# 3. Retrieval: Get Database Schema
# -----------------------------
def get_schema(conn):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """)

    tables = cursor.fetchall()

    schema = ""

    for table in tables:

        table_name = table[0]

        cursor.execute(
            f"PRAGMA table_info({table_name})"
        )

        columns = cursor.fetchall()

        schema += f"\nTable: {table_name}\n"

        for column in columns:
            schema += f"- {column[1]} ({column[2]})\n"

    return schema


# -----------------------------
# 4. Query Generation: NL -> SQL
# -----------------------------
def generate_sql(question, schema):

    prompt = f"""
You are an expert SQL generator.

Convert the user's natural language question
into SQLite SQL.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

Rules:
1. Return ONLY SQL.
2. Do not use markdown.
3. Do not explain the SQL.
4. Use only tables and columns from the schema.
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    sql = response.text.strip()

    # Remove markdown if model adds it
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")

    return sql.strip()


# -----------------------------
# 5. Execute SQL
# -----------------------------
def execute_sql(conn, sql):

    cursor = conn.cursor()

    try:

        cursor.execute(sql)

        results = cursor.fetchall()

        return results

    except Exception as e:

        return f"SQL Error: {e}"


# -----------------------------
# 6. Main Workflow
# -----------------------------
def main():

    conn = create_database()

    schema = get_schema(conn)

    print("Database Schema:")
    print(schema)

    question = input(
        "\nAsk a question about employees: "
    )

    print("\nGenerating SQL...")

    sql = generate_sql(
        question,
        schema
    )

    print("\nGenerated SQL:")
    print(sql)

    print("\nExecuting SQL...")

    results = execute_sql(
        conn,
        sql
    )

    print("\nResult:")

    if isinstance(results, str):
        print(results)
    elif not results:
        print("(no rows returned)")
    else:
        for row in results:
            print(row)

    conn.close()


if __name__ == "__main__":
    main()