import tkinter as tk
from tkinter import messagebox
from app.ai.symptom_checker import ManualSymptomChecker
from app.database import db_manager
from datetime import datetime

class PatientForm(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#ecf0f1")
        self.master = master
        self.app = app
        self.username = username
        self.predictor = ManualSymptomChecker("app/data/symptoms_dataset.csv")
        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        # Header Section
        header_frame = tk.Frame(self, bg="#2c3e50")
        header_frame.pack(fill="x")

        tk.Label(
            header_frame,
            text="🩺 Human Symptom Checkup",
            font=("Segoe UI", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=20)

        tk.Label(
            header_frame,
            text=f"Logged in as: {self.username}",
            font=("Segoe UI", 10),
            bg="#2c3e50",
            fg="#bdc3c7"
        ).pack(pady=(0, 10))

        # Form Section
        form_frame = tk.Frame(self, bg="#ecf0f1")
        form_frame.pack(pady=30)

        tk.Label(
            form_frame,
            text="📝 Describe your symptoms below:",
            font=("Segoe UI", 13, "bold"),
            bg="#ecf0f1",
            fg="#34495e"
        ).pack(pady=(0, 10))

        self.symptom_entry = tk.Text(
            form_frame,
            height=7,
            width=80,
            font=("Segoe UI", 11),
            wrap="word",
            bd=2,
            relief="groove",
            padx=10,
            pady=10
        )
        self.symptom_entry.pack(pady=(0, 20))

        # Buttons Section
        button_frame = tk.Frame(form_frame, bg="#ecf0f1")
        button_frame.pack()

        tk.Button(
            button_frame,
            text="🔍 Run Symptom Checker",
            font=("Segoe UI", 11, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            padx=20,
            pady=10,
            bd=0,
            relief="flat",
            width=30,
            command=self.check_symptoms
        ).pack(pady=(0, 10))

        tk.Button(
            button_frame,
            text="🔙 Back to Dashboard",
            font=("Segoe UI", 10, "bold"),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            padx=20,
            pady=8,
            bd=0,
            relief="flat",
            width=25,
            command=self.back_to_dashboard
        ).pack(pady=(0, 30))

    def check_symptoms(self):
        symptoms = self.symptom_entry.get("1.0", tk.END).strip()

        if not symptoms:
            messagebox.showwarning("Input Required", "Please enter your symptoms before checking.")
            return

        try:
            diagnosis_message = self.predictor.predict(symptoms)

            if "**" in diagnosis_message:
                start = diagnosis_message.find("**") + 2
                end = diagnosis_message.find("**", start)
                diagnosis_only = diagnosis_message[start:end]
            else:
                diagnosis_only = "Unknown"

            db_manager.save_diagnosis(
                self.username,
                symptoms,
                diagnosis_only,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            messagebox.showinfo("Diagnosis Result", diagnosis_message)

        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed:\n{e}")

    def back_to_dashboard(self):
        from app.gui.patient_dashboard import PatientDashboard
        self.app._switch_frame(PatientDashboard, self.app, self.username)

    def new_checkup(self):
        from app.gui.patient_form import PatientForm
        self.app._switch_frame(PatientForm, self.app, self.username)
