import sqlite3

DB_PATH = 'users.db'

def connect_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT   
            
                   
        )
    """)
    conn.commit()
    conn.close()

    # conn = sqlite3.connect('users.db')
    # cursor = conn.cursor()
    # cursor.execute("ALTER TABLE users ADD COLUMN city TEXT")

    # conn.commit()
    # conn.close()

def update_user(user_id, name, age, email, phone, city):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(""" 
        UPDATE users
        SET name = ?, age = ?, email = ?, phone = ?, city = ?
        WHERE id = ?
    """,          (name, age, email, phone, city, user_id))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated

def update_user_city(user_id, new_city):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET city = ?
        WHERE id = ?
    """,          (new_city, user_id))
    conn.commit()
    count = cursor.rowcount
    conn.close()
    return count