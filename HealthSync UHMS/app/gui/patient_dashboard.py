import tkinter as tk
from tkinter import messagebox
from app.gui.health_summary_view import export_latest_health_pdf

class PatientDashboard(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#ecf7f9")  # Softer light teal background
        self.master = master
        self.app = app
        self.username = username
        self.pack(fill="both", expand=True)

        self.build_ui()

    def build_ui(self):
        # Main container (like a card)
        card = tk.Frame(
            self,
            bg="white",
            bd=0,
            highlightbackground="#d6eaf8",
            highlightthickness=2
        )
        card.place(relx=0.5, rely=0.05, anchor="n", relwidth=0.85, relheight=0.9)

        # Header
        tk.Label(
            card,
            text=f"🧍 Human Health Support – {self.username}",
            font=("Segoe UI", 22, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=(20, 10))

        # Divider line
        tk.Frame(card, bg="#3498db", height=2).pack(fill="x", padx=40, pady=(0, 30))

        # Button styling
        btn_config = {
            "font": ("Segoe UI", 14, "bold"),
            "bg": "#3498db",
            "fg": "white",
            "activebackground": "#2980b9",
            "activeforeground": "white",
            "width": 35,
            "height": 2,
            "bd": 0,
            "relief": "flat",
        }

        # Buttons list
        buttons = [
            ("📝 New Symptom Checkup", self.new_checkup),
            ("📂 View Diagnosis History", self.view_history),
            ("📊 View Health Summary", self.view_summary),
            ("🧾 Export Health Report (PDF)", self.export_pdf),
            ("🏥 Find Nearby Clinics", self.find_clinics),
        ]

        # Create buttons with hover effect
        for text, command in buttons:
            b = tk.Button(card, text=text, command=command, **btn_config)
            b.pack(pady=8)
            self.add_hover_effect(b, "#3498db", "#2980b9")

        # Back button
        back_btn = tk.Button(
            card,
            text="🔙 Back to Main Menu",
            font=("Segoe UI", 13, "bold"),
            bg="#7f8c8d",
            fg="white",
            activebackground="#616a6b",
            activeforeground="white",
            width=25,
            height=2,
            bd=0,
        )
        back_btn.pack(pady=(40, 20))
        back_btn.config(command=self.back_to_menu)
        self.add_hover_effect(back_btn, "#7f8c8d", "#5d6d6f")

    def add_hover_effect(self, widget, normal_color, hover_color):
        """Adds hover color effect to buttons."""
        def on_enter(e):
            widget.config(bg=hover_color)
        def on_leave(e):
            widget.config(bg=normal_color)
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

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
