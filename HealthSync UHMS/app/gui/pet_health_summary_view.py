import tkinter as tk
from tkinter import messagebox
from collections import Counter
from datetime import datetime
import sqlite3
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.database import db_manager
from app.auth.user_manager import DB_PATH

class PetHealthSummaryView(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#f4f9fb")
        self.master = master
        self.app = app
        self.username = username
        self.pack(fill="both", expand=True)
        self.selected_pet = None

        self.build_ui()
        self.load_pet_names()

    def build_ui(self):
        tk.Label(
            self,
            text=f"🐾 Pet Health Summary – {self.username}",
            font=("Segoe UI", 20, "bold"),
            bg="#f4f9fb",
            fg="#2c3e50"
        ).pack(pady=(30, 10))

        # Pet Selection Dropdown
        dropdown_frame = tk.Frame(self, bg="#f4f9fb")
        dropdown_frame.pack(pady=(0, 20))

        tk.Label(
            dropdown_frame,
            text="Select a Pet:",
            font=("Segoe UI", 11, "bold"),
            bg="#f4f9fb"
        ).pack(side="left", padx=(10, 5))

        self.pet_var = tk.StringVar()
        self.pet_menu = tk.OptionMenu(dropdown_frame, self.pet_var, ())
        self.pet_menu.config(font=("Segoe UI", 10), width=30)
        self.pet_menu.pack(side="left", padx=5)

        tk.Button(
            dropdown_frame,
            text="📄 Load Summary",
            font=("Segoe UI", 10, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            command=self.load_summary
        ).pack(side="left", padx=10)

        # Summary text
        self.summary_text = tk.Text(self, height=12, width=70, font=("Segoe UI", 10), wrap="word", bg="white")
        self.summary_text.pack(padx=20, pady=10)

        # Chart area
        self.chart_frame = tk.Frame(self, bg="#f4f9fb")
        self.chart_frame.pack(pady=(0, 10))

        # Buttons
        button_frame = tk.Frame(self, bg="#f4f9fb")
        button_frame.pack()

        tk.Button(
            button_frame,
            text="📤 Export Pet Report (PDF)",
            font=("Segoe UI", 10, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#1e8449",
            width=30,
            height=2,
            bd=0,
            command=self.export_pdf
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="🔙 Back to Dashboard",
            font=("Segoe UI", 10, "bold"),
            bg="#7f8c8d",
            fg="white",
            activebackground="#616a6b",
            width=25,
            height=2,
            bd=0,
            command=self.back_to_dashboard
        ).grid(row=0, column=1, padx=10)

    def load_pet_names(self):
        # Ensure pets table exists
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_username TEXT NOT NULL,
                pet_name TEXT NOT NULL,
                species TEXT NOT NULL,
                breed TEXT,
                age INTEGER,
                description TEXT,
                image_path TEXT
            )
        """)
        cursor.execute("SELECT pet_name FROM pets WHERE owner_username = ?", (self.username,))
        pets = cursor.fetchall()
        conn.close()

        self.pet_names = [pet[0] for pet in pets]
        self.pet_var.set(self.pet_names[0] if self.pet_names else "")

        # Refresh dropdown
        menu = self.pet_menu["menu"]
        menu.delete(0, "end")
        for name in self.pet_names:
            menu.add_command(label=name, command=lambda value=name: self.pet_var.set(value))

    def load_summary(self):
        pet_name = self.pet_var.get().strip()
        if not pet_name:
            messagebox.showwarning("No Pet Selected", "Please select a pet to load summary.")
            return

        self.selected_pet = pet_name

        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pet_checkups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                pet_name TEXT NOT NULL,
                date TEXT NOT NULL,
                symptoms TEXT,
                diagnosis TEXT
            )
        """)
        cursor.execute("""
            SELECT date, symptoms, diagnosis FROM pet_checkups
            WHERE username = ? AND pet_name = ?
        """, (self.username, pet_name))
        rows = cursor.fetchall()
        conn.close()

        self.summary_text.delete("1.0", tk.END)
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        if not rows:
            self.summary_text.insert(tk.END, f"No checkup history found for {pet_name}.")
            return

        diagnoses = [row[2] for row in rows]
        symptoms = [s.strip() for row in rows for s in row[1].split(",")]
        dates = [row[0] for row in rows]
        total = len(rows)

        most_recent = dates[-1]
        top_diagnosis = Counter(diagnoses).most_common(1)
        top_symptoms = Counter(symptoms).most_common(5)

        summary = (
            f"🐶 Pet Name: {pet_name}\n"
            f"📝 Total Checkups: {total}\n"
            f"📆 Most Recent: {most_recent}\n\n"
            f"🏥 Most Frequent Condition:\n"
            f"   → {top_diagnosis[0][0]} ({top_diagnosis[0][1]} times)\n\n"
            f"😺 Common Symptoms:\n"
        )
        for sym, count in top_symptoms:
            summary += f"   • {sym} ({count} times)\n"

        self.summary_text.insert(tk.END, summary)

        self.render_chart(diagnoses)

    def render_chart(self, diagnoses):
        if not diagnoses:
            return

        counts = Counter(diagnoses).most_common(5)
        labels, values = zip(*counts)

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.barh(labels, values, color="#9b59b6")
        ax.set_title("Top Pet Conditions")
        ax.set_xlabel("Frequency")
        ax.invert_yaxis()
        fig.tight_layout()

        self.chart_path = f"pet_chart_{self.username}_{self.selected_pet}.png"
        fig.savefig(self.chart_path)
        plt.close(fig)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def export_pdf(self):
        try:
            from PIL import Image
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_path = f"pet_health_report_{self.username}_{self.selected_pet}_{timestamp}.pdf"
            c = canvas.Canvas(file_path, pagesize=A4)
            width, height = A4
            margin = 50
            y = height - margin

            c.setFont("Helvetica-Bold", 16)
            c.drawString(margin, y, f"🐾 Pet Health Report for {self.selected_pet}")
            y -= 30

            c.setFont("Helvetica", 10)
            for line in self.summary_text.get("1.0", tk.END).splitlines():
                if line.strip():
                    c.drawString(margin, y, line.strip())
                    y -= 15
                    if y < 100:
                        c.showPage()
                        y = height - margin

            if os.path.exists(self.chart_path):
                if y < 250:
                    c.showPage()
                    y = height - margin
                c.drawImage(self.chart_path, margin, y - 220, width=400, height=200)
                os.remove(self.chart_path)

            c.setFont("Helvetica-Oblique", 8)
            c.setFillColorRGB(0.3, 0.3, 0.3)
            c.drawString(margin, 40, "*This report is for informational purposes only. Always consult a licensed vet.")

            c.save()
            messagebox.showinfo("PDF Exported", f"PDF saved as:\n{os.path.abspath(file_path)}")

        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not export PDF:\n{e}")

    def back_to_dashboard(self):
        from app.gui.pet_dashboard import PetDashboard
        self.app._switch_frame(PetDashboard, self.app, self.username)
