import sqlite3
from datetime import datetime

def create_diagnosis_table():
    conn = sqlite3.connect("data/patients.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS diagnosis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            input_symptoms TEXT,
            diagnosis TEXT,
            date TEXT
        )
    """)
    conn.commit()
    conn.close()
