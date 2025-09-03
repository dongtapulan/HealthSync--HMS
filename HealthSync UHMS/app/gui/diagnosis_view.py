import tkinter as tk
from tkinter import ttk
from app.database import db_manager

class DiagnosisHistoryView(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#eef2f7")  # soft gray-blue background
        self.master = master
        self.app = app
        self.username = username
        self.pack(fill="both", expand=True)
        self.build_ui()
        self.load_history()

    def build_ui(self):
        # Card container
        card = tk.Frame(self, bg="white", bd=0, highlightbackground="#d6e4f0", highlightthickness=2)
        card.place(relx=0.5, rely=0.05, anchor="n", relwidth=0.9, relheight=0.85)

        # Header
        tk.Label(
            card,
            text=f"📂 Diagnosis History – {self.username}",
            font=("Segoe UI", 18, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=(15, 8))

        # Divider
        tk.Frame(card, bg="#3498db", height=2).pack(fill="x", padx=30, pady=(0, 15))

        # Treeview setup
        columns = ("date", "symptoms", "diagnosis")
        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=12)

        self.tree.heading("date", text="Date/Time")
        self.tree.heading("symptoms", text="Symptoms")
        self.tree.heading("diagnosis", text="Diagnosis/Result")

        self.tree.column("date", width=140, anchor="center")
        self.tree.column("symptoms", width=250, anchor="w")
        self.tree.column("diagnosis", width=300, anchor="w")

        # Style
        style = ttk.Style()
        style.configure("Treeview",
                        font=("Segoe UI", 11),
                        rowheight=28)
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 11, "bold"),
                        background="#3498db",
                        foreground="white")
        style.map("Treeview",
                  background=[("selected", "#2980b9")],
                  foreground=[("selected", "white")])

        # Add striped rows
        self.tree.tag_configure("oddrow", background="#f9f9f9")
        self.tree.tag_configure("evenrow", background="#eef6fb")

        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

        # Back button
        back_btn = tk.Button(
            card,
            text="🔙 Back to Dashboard",
            font=("Segoe UI", 11, "bold"),
            bg="#7f8c8d",
            fg="white",
            activebackground="#616a6b",
            activeforeground="white",
            width=22,
            height=2,
            bd=0,
            command=self.back_to_dashboard
        )
        back_btn.pack(pady=(15, 20))

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

            rows = cursor.fetchall()
            for i, row in enumerate(rows):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree.insert("", "end", values=row, tags=(tag,))

            conn.close()
        except Exception as e:
            print(f"Error loading history: {e}")

    def back_to_dashboard(self):
        from app.gui.patient_dashboard import PatientDashboard
        self.app._switch_frame(PatientDashboard, self.app, self.username)
