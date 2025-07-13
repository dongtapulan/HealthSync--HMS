import tkinter as tk
from tkinter import messagebox
from app.ai.symptom_checker import ManualSymptomChecker
from app.database import db_manager
from datetime import datetime

class PatientForm(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#f4f9fb")
        self.master = master
        self.app = app
        self.username = username
        self.predictor = ManualSymptomChecker("app/data/symptoms_dataset.csv")
        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        tk.Label(
            self,
            text="🩺 Human Symptom Checkup",
            font=("Segoe UI", 22, "bold"),
            bg="#f4f9fb",
            fg="#2c3e50"
        ).pack(pady=(30, 10))

        tk.Label(
            self,
            text=f"Patient: {self.username}",
            font=("Segoe UI", 12),
            bg="#f4f9fb",
            fg="#7f8c8d"
        ).pack(pady=(0, 20))

        tk.Label(
            self,
            text="Please describe your symptoms below:",
            font=("Segoe UI", 12, "bold"),
            bg="#f4f9fb",
            fg="#34495e"
        ).pack(pady=(10, 5))

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
            text="🔍 Run Symptom Checker",
            font=("Segoe UI", 12, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            width=30,
            height=2,
            bd=0,
            command=self.check_symptoms
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

    def check_symptoms(self):
        symptoms = self.symptom_entry.get("1.0", tk.END).strip()

        if not symptoms:
            messagebox.showwarning("Input Required", "Please enter your symptoms before checking.")
            return

        try:
            # Get full prediction message (with disclaimer + diagnosis)
            diagnosis_message = self.predictor.predict(symptoms)

            # Extract diagnosis from "**...**" if available
            if "**" in diagnosis_message:
                start = diagnosis_message.find("**") + 2
                end = diagnosis_message.find("**", start)
                diagnosis_only = diagnosis_message[start:end]
            else:
                diagnosis_only = "Unknown"

            # Save to DB
            db_manager.save_diagnosis(
                self.username,
                symptoms,
                diagnosis_only,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            # Show result popup
            messagebox.showinfo("Diagnosis Result", diagnosis_message)

        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed:\n{e}")

    def back_to_dashboard(self):
        from app.gui.patient_dashboard import PatientDashboard
        self.app._switch_frame(PatientDashboard, self.app, self.username)

    def new_checkup(self):
        from app.gui.patient_form import PatientForm
        self.app._switch_frame(PatientForm, self.app, self.username)
