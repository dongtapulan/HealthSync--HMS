import tkinter as tk
from tkinter import messagebox
from app.gui.health_summary_view import export_latest_health_pdf

class PatientDashboard(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#f9f9ff")
        self.master = master
        self.app = app
        self.username = username
        self.pack(fill="both", expand=True)

        self.build_ui()

    def build_ui(self):
        # Create an inner container frame for padding and spacing
        inner_frame = tk.Frame(self, bg="#f9f9ff")
        inner_frame.place(relx=0.5, rely=0.05, anchor="n")

        tk.Label(
            inner_frame,
            text=f"🧍 Human Health Support – {self.username}",
            font=("Segoe UI", 20, "bold"),
            bg="#f9f9ff",
            fg="#2c3e50"
        ).pack(pady=(10, 30))

        # Standard button config
        btn_config = {
            "font": ("Segoe UI", 13, "bold"),
            "bg": "#3498db",
            "fg": "white",
            "activebackground": "#2980b9",
            "width": 30,
            "height": 2,
            "bd": 0
        }

        # List of buttons with commands
        buttons = [
            ("📝 New Symptom Checkup", self.new_checkup),
            ("📂 View Diagnosis History", self.view_history),
            ("📊 View Health Summary", self.view_summary),
            ("🧾 Export Health Report (PDF)", self.export_pdf),
            ("🏥 Find Nearby Clinics", self.find_clinics),
        ]

        for text, command in buttons:
            tk.Button(inner_frame, text=text, command=command, **btn_config).pack(pady=6)

        # Separate Back button config
        back_btn = tk.Button(
            inner_frame,
            text="🔙 Back to Main Menu",
            font=("Segoe UI", 13, "bold"),
            bg="#7f8c8d",
            fg="white",
            activebackground="#616a6b",
            width=30,
            height=2,
            bd=0,
            command=self.back_to_menu
        )
        back_btn.pack(pady=(40, 10))

    # Placeholder functions
    def new_checkup(self):
        from app.gui.patient_form import PatientForm
        self.app._switch_frame(PatientForm, self.app, self.username)

    def view_history(self):
        from app.gui.diagnosis_view import DiagnosisHistoryView
        self.app._switch_frame(DiagnosisHistoryView, self.app, self.username)


    def view_summary(self):
        from app.gui.health_summary_view import HealthSummaryView
        self.app._switch_frame(HealthSummaryView, self.app, self.username)

    def export_pdf(self):
        try:
            export_latest_health_pdf(self.username)
            messagebox.showinfo("Exported", "✅ Health report exported successfully!")
        except Exception as e:
            messagebox.showerror("Export Failed", f"⚠️ Something went wrong:\n{e}")
    
    def find_clinics(self):
        from app.gui.clinic_finder import ClinicFinder
        self.app._switch_frame(ClinicFinder, self.app, self.username)

    def back_to_menu(self):
        self.app.show_main_menu(self.username)
