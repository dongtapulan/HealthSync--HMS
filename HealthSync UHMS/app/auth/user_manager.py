# app/auth/user_manager.py

import sqlite3
from app.auth.auth_utils import hash_password, verify_password
from app.auth.roles import ROLE_ADMIN, ROLE_PATIENT

DB_PATH = "app/data/patients.db" 


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Users table (already present)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)
    # Adoption list table (add this)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS adoption_list (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_username TEXT NOT NULL,
            pet_name TEXT NOT NULL,
            species TEXT NOT NULL,
            breed TEXT,
            age INTEGER,
            description TEXT
        )
    """)
    # Ensure admin user exists
    cursor.execute("SELECT 1 FROM users WHERE username = ?", ("admin",))
    if not cursor.fetchone():
        from app.auth.auth_utils import hash_password
        admin_hash = hash_password("admin123")
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",

            ("admin", admin_hash, "admin")
        )
    conn.commit()
    conn.close()

def create_user_table():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'patient'))
            );
        ''')
        conn.commit()

def register_user(username: str, password: str, role=ROLE_PATIENT):
    hashed = hash_password(password)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, hashed, role)
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # username taken

def authenticate_user(username: str, password: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        if row:
            stored_hash, role = row
            if verify_password(password, stored_hash):
                return role  # login success
    return None  # login failed

def user_exists(username: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        return cursor.fetchone() is not None
