import psycopg2

import os
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn




def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS expenses(
            id SERIAL PRIMARY KEY,
            amount NUMERIC(10,2) NOT NULL,
            category VARCHAR(100) NOT NULL,
            date DATE NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        """
    )

    conn.commit()
    conn.close()


def create_expense(amount, category, date, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses (amount, category, date, user_id)
        VALUES (%s, %s, %s, %s)
    """, (amount, category, date, user_id))

    conn.commit()
    cursor.close()
    conn.close()


def get_all_expenses():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM expenses
    """)

    expenses = cursor.fetchall()

    cursor.close()
    conn.close()
    return expenses


def get_expense_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM expenses
        WHERE id = %s
    """, (id,))

    expense = cursor.fetchone()

    cursor.close()
    conn.close()
    return expense


def get_expenses_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * 
        FROM expenses 
        WHERE user_id = %s
    """, (user_id,))

    expenses = cursor.fetchall()

    cursor.close()
    conn.close()
    return expenses


def total_expenses_by_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = %s
    """, (user_id,))

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return total


def update_expense(id, amount, category, date, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE expenses
        SET amount = %s,
            category = %s,
            date = %s,
            user_id = %s
        WHERE id = %s
    """, (amount, category, date, user_id, id))

    conn.commit()
    cursor.close()
    conn.close()


def delete_expense(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM expenses
        WHERE id = %s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()


def total_by_category():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM expenses
        GROUP BY category
    """)

    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def total_by_month():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT DATE_TRUNC('month', date) AS month, SUM(amount)
        FROM expenses
        GROUP BY month
    """)

    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def add_user(name, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (name, email)
        VALUES (%s, %s)
    """, (name, email))

    conn.commit()
    cursor.close()
    conn.close()








if __name__ == "__main__":
    conn = get_connection()
    print("Connection successful!")
    init_db()
    conn.close()