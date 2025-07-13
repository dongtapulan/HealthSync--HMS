import sqlite3
import os
from datetime import datetime

# Path to your local database
DB_PATH = "app/data/patients.db"

# Make sure the directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Connection helper
def get_connection():
    return sqlite3.connect(DB_PATH)

# Initialize database tables
def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    # Diagnosis history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diagnosis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            date TEXT NOT NULL,
            symptoms TEXT NOT NULL,
            diagnosis TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# Save a diagnosis entry for a patient
def save_diagnosis(username, symptoms, diagnosis, date=None):
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO diagnosis_history (username, date, symptoms, diagnosis)
        VALUES (?, ?, ?, ?)
    """, (username, date, symptoms, diagnosis))
    conn.commit()
    conn.close()

# Fetch diagnosis history for a specific user
def get_diagnosis_history(username):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, symptoms, diagnosis
        FROM diagnosis_history
        WHERE username = ?
        ORDER BY date DESC
    """, (username,))
    history = cursor.fetchall()
    conn.close()
    return history
