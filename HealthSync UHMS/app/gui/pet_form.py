import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import csv
import os
import sqlite3
from app.database import db_manager
from app.auth.user_manager import DB_PATH

class PetForm(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#f4f9fb")
        self.master = master
        self.app = app
        self.username = username
        self.csv_path = os.path.join("app", "data", "vet_symptoms_dataset.csv")
        self.pet_data = []
        self.pack(fill="both", expand=True)

        self.build_ui()
        self.ensure_pet_checkups_table()
        self.load_pet_list()

    def build_ui(self):
        tk.Label(
            self,
            text="🐾 Pet Symptom Checker",
            font=("Segoe UI", 22, "bold"),
            bg="#f4f9fb",
            fg="#2c3e50"
        ).pack(pady=(30, 10))

        tk.Label(
            self,
            text=f"Veterinary Mode – User: {self.username}",
            font=("Segoe UI", 12),
            bg="#f4f9fb",
            fg="#7f8c8d"
        ).pack(pady=(0, 20))

        # Pet Selector
        selector_frame = tk.Frame(self, bg="#f4f9fb")
        selector_frame.pack(pady=10)

        tk.Label(
            selector_frame, text="Select a Pet:",
            font=("Segoe UI", 11, "bold"), bg="#f4f9fb"
        ).pack(side="left", padx=5)

        self.selected_pet_var = tk.StringVar()
        self.pet_menu = tk.OptionMenu(selector_frame, self.selected_pet_var, ())
        self.pet_menu.config(font=("Segoe UI", 10), width=30)
        self.pet_menu.pack(side="left", padx=5)
        self.selected_pet_var.trace("w", self.update_pet_fields)

        # Pet Name (read-only)
        tk.Label(self, text="Pet Name:", font=("Segoe UI", 11, "bold"), bg="#f4f9fb").pack(pady=(10, 0))
        self.pet_name_entry = tk.Entry(self, font=("Segoe UI", 11), width=40, state="readonly")
        self.pet_name_entry.pack(pady=5)

        # Animal Type (read-only)
        tk.Label(self, text="Animal Type (e.g., Dog, Cat):", font=("Segoe UI", 11, "bold"), bg="#f4f9fb").pack(pady=(10, 0))
        self.pet_type_entry = tk.Entry(self, font=("Segoe UI", 11), width=40, state="readonly")
        self.pet_type_entry.pack(pady=5)

        # Symptoms
        tk.Label(
            self,
            text="Describe Symptoms:",
            font=("Segoe UI", 11, "bold"),
            bg="#f4f9fb"
        ).pack(pady=(15, 5))

        self.symptom_entry = tk.Text(
            self,
            height=6,
            width=70,
            font=("Segoe UI", 11),
            wrap="word",
            bd=1,
            relief="solid"
        )
        self.symptom_entry.pack(pady=10)

        tk.Button(
            self,
            text="🔍 Analyze Pet Symptoms",
            font=("Segoe UI", 12, "bold"),
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            width=30,
            height=2,
            bd=0,
            command=self.analyze_pet_symptoms
        ).pack(pady=20)

        tk.Button(
            self,
            text="🔙 Back to Dashboard",
            font=("Segoe UI", 11, "bold"),
            bg="#7f8c8d",
            fg="white",
            activebackground="#616a6b",
            width=25,
            height=2,
            bd=0,
            command=self.back_to_dashboard
        ).pack(pady=(10, 30))

    def ensure_pet_checkups_table(self):
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
        conn.commit()
        conn.close()

    def load_pet_list(self):
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
        cursor.execute("SELECT pet_name, species FROM pets WHERE owner_username = ?", (self.username,))
        self.pet_data = cursor.fetchall()
        conn.close()

        menu = self.pet_menu["menu"]
        menu.delete(0, "end")
        if not self.pet_data:
            self.selected_pet_var.set("")
            self.pet_name_entry.config(state="normal")
            self.pet_name_entry.delete(0, tk.END)
            self.pet_name_entry.insert(0, "")
            self.pet_name_entry.config(state="readonly")
            self.pet_type_entry.config(state="normal")
            self.pet_type_entry.delete(0, tk.END)
            self.pet_type_entry.insert(0, "")
            self.pet_type_entry.config(state="readonly")
            messagebox.showinfo("No Pets Found", "You haven't added any pets yet.\nPlease add a pet first via Pet Profile.")
            return

        for pet in self.pet_data:
            menu.add_command(label=pet[0], command=lambda value=pet[0]: self.selected_pet_var.set(value))
        self.selected_pet_var.set(self.pet_data[0][0])  # Set to first pet

    def update_pet_fields(self, *args):
        selected = self.selected_pet_var.get()
        for name, species in self.pet_data:
            if name == selected:
                self.pet_name_entry.config(state="normal")
                self.pet_name_entry.delete(0, tk.END)
                self.pet_name_entry.insert(0, name)
                self.pet_name_entry.config(state="readonly")

                self.pet_type_entry.config(state="normal")
                self.pet_type_entry.delete(0, tk.END)
                self.pet_type_entry.insert(0, species)
                self.pet_type_entry.config(state="readonly")
                break

    def analyze_pet_symptoms(self):
        pet_name = self.pet_name_entry.get().strip()
        pet_type = self.pet_type_entry.get().strip()
        symptoms = self.symptom_entry.get("1.0", tk.END).strip().lower()

        if not pet_name or not pet_type or not symptoms:
            messagebox.showwarning("Incomplete Info", "Please complete all fields before analysis.")
            return

        matched_condition = "Unknown Condition"
        care_instructions = "No advice available. Please consult a veterinarian."

        if os.path.exists(self.csv_path):
            with open(self.csv_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    keyword = row["keyword"].strip().lower()
                    if keyword in symptoms:
                        matched_condition = row["suggested_condition"]
                        care_instructions = row["care_instructions"]
                        break

        # Save to database
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pet_checkups (username, pet_name, date, symptoms, diagnosis)
            VALUES (?, ?, ?, ?, ?)
        """, (
            self.username,
            pet_name,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            symptoms,
            matched_condition
        ))
        conn.commit()
        conn.close()

        result = (
            f"🐶 Pet Name: {pet_name}\n"
            f"📘 Animal Type: {pet_type}\n\n"
            f"📝 Reported Symptoms:\n{symptoms}\n\n"
            f"🧠 Possible Condition: {matched_condition}\n\n"
            f"📋 Care Instructions:\n{care_instructions}"
        )

        messagebox.showinfo("Diagnosis Result", result)

    def back_to_dashboard(self):
        from app.gui.pet_dashboard import PetDashboard
        self.app._switch_frame(PetDashboard, self.app, self.username)
