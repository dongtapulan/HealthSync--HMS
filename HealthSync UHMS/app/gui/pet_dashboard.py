import tkinter as tk
from app.gui.pet_health_summary_view import PetHealthSummaryView

class PetDashboard(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#eefaf2")  # Light mint green background
        self.master = master
        self.app = app
        self.username = username
        self.pack(fill="both", expand=True)

        self.build_ui()

    def build_ui(self):
        # Card container
        card = tk.Frame(
            self,
            bg="white",
            bd=0,
            highlightbackground="#c8e6c9",
            highlightthickness=2
        )
        card.place(relx=0.5, rely=0.05, anchor="n", relwidth=0.85, relheight=0.9)

        # Header
        tk.Label(
            card,
            text=f"🐶 Pet Health Support – {self.username}",
            font=("Segoe UI", 22, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=(20, 10))

        # Divider line
        tk.Frame(card, bg="#2ecc71", height=2).pack(fill="x", padx=40, pady=(0, 30))

        # Button style
        btn_config = {
            "font": ("Segoe UI", 12, "bold"),
            "bg": "#2ecc71",
            "fg": "white",
            "activeforeground": "white",
            "width": 28,
            "height": 2,
            "bd": 0,
            "relief": "flat",
        }

        # Buttons list
        buttons = [
            ("🩺 New Pet Checkup", self.pet_checkup),
            ("📋 View/Add Pet Profiles", self.pet_profiles),
            ("🏠 Adoption Requests", self.adoption_center),
            ("📖 My Adopted Pets", self.adopted_history),
            ("📊 Pet Health Summary", self.pet_health_summary),
            ("📍 Find Vet Clinics Nearby", self.vet_clinic_finder),
        ]

        for text, command in buttons:
            b = tk.Button(card, text=text, command=command, **btn_config)
            b.pack(pady=6)
            self.add_hover_effect(b, "#2ecc71", "#27ae60")

        # Back button
        back_btn = tk.Button(
            card,
            text="🔙 Back to Main Menu",
            font=("Segoe UI", 12, "bold"),
            bg="#7f8c8d",
            fg="white",
            activebackground="#616a6b",
            activeforeground="white",
            width=24,
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

    # Navigation functions
    def pet_checkup(self):
        from app.gui.pet_form import PetForm
        self.app._switch_frame(PetForm, self.app, self.username)

    def pet_profiles(self):
        from app.gui.pet_profile import PetProfile
        self.app._switch_frame(PetProfile, self.app, self.username)

    def adoption_center(self):
        from app.gui.adoption_dashboard import AdoptionDashboard
        self.app._switch_frame(AdoptionDashboard, self.app, self.username)

    def pet_health_summary(self):
        from app.gui.pet_health_summary_view import PetHealthSummaryView
        self.app._switch_frame(PetHealthSummaryView, self.app, self.username)

    def adopted_history(self):
        from app.gui.adopted_pets_history import AdoptedPetsHistory
        self.app._switch_frame(AdoptedPetsHistory, self.app, self.username)

    def vet_clinic_finder(self):
        from app.gui.vet_clinic_finder import VetClinicFinder
        self.app._switch_frame(VetClinicFinder, self.app, self.username)

    def back_to_menu(self):
        self.app.show_main_menu(self.username)
