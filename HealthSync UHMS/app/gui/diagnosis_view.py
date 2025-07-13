import tkinter as tk
from tkinter import ttk
from app.database import db_manager

class DiagnosisHistoryView(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#f9f9ff")
        self.master = master
        self.app = app
        self.username = username
        self.pack(fill="both", expand=True)
        self.build_ui()
        self.load_history()

    def build_ui(self):
        tk.Label(
            self,
            text=f"📂 Diagnosis History – {self.username}",
            font=("Segoe UI", 20, "bold"),
            bg="#f9f9ff",
            fg="#2c3e50"
        ).pack(pady=(20, 10))

        # Treeview setup
        columns = ("date", "symptoms", "diagnosis")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        self.tree.heading("date", text="Date/Time")
        self.tree.heading("symptoms", text="Symptoms")
        self.tree.heading("diagnosis", text="Diagnosis/Result")

        self.tree.column("date", width=160, anchor="center")
        self.tree.column("symptoms", width=300, anchor="w")
        self.tree.column("diagnosis", width=400, anchor="w")

        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        # Back button
        tk.Button(
            self,
            text="🔙 Back to Dashboard",
            font=("Segoe UI", 12, "bold"),
            bg="#7f8c8d",
            fg="white",
            activebackground="#616a6b",
            width=25,
            height=2,
            bd=0,
            command=self.back_to_dashboard
        ).pack(pady=20)

    def load_history(self):
        self.tree.delete(*self.tree.get_children())

        try:
            conn = db_manager.get_connection()
            cursor = conn.cursor()

            # Ensure table exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS diagnosis_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    date TEXT,
                    symptoms TEXT,
                    diagnosis TEXT
                )
            """)

            # Fetch and display history
            cursor.execute("""
                SELECT date, symptoms, diagnosis
                FROM diagnosis_history
                WHERE username = ?
                ORDER BY date DESC
            """, (self.username,))
            for row in cursor.fetchall():
                self.tree.insert("", "end", values=row)

            conn.close()
        except Exception as e:
            print(f"Error loading history: {e}")  # Debug print

    def back_to_dashboard(self):
        from app.gui.patient_dashboard import PatientDashboard
        self.app._switch_frame(PatientDashboard, self.app, self.username)
