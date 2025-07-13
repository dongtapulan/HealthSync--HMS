import tkinter as tk
from app.gui.pet_health_summary_view import PetHealthSummaryView

class PetDashboard(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#f9f9ff")
        self.master = master
        self.app = app
        self.username = username
        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        tk.Label(
            self,
            text=f"🐶 Pet Health Support – {self.username}",
            font=("Segoe UI", 20, "bold"),
            bg="#f9f9ff",
            fg="#2c3e50"
        ).pack(pady=30)

        btn_config = {
            "font": ("Segoe UI", 13, "bold"),
            "bg": "#2ecc71",
            "fg": "white",
            "activebackground": "#27ae60",
            "width": 30,
            "height": 2,
            "bd": 0,
            "pady": 5
        }

        tk.Button(self, text="🩺 New Pet Checkup", command=self.pet_checkup, **btn_config).pack(pady=5)
        tk.Button(self, text="📋 View/Add Pet Profiles", command=self.pet_profiles, **btn_config).pack(pady=5)
        tk.Button(self, text="🏠 Adoption Requests", command=self.adoption_center, **btn_config).pack(pady=5)
        tk.Button(self, text="📖 My Adopted Pets", command=self.adopted_history, **btn_config).pack(pady=5)
        tk.Button(self, text="📊 Pet Health Summary", command=self.pet_health_summary, **btn_config).pack(pady=5)
        tk.Button(self, text="📍 Find Vet Clinics Nearby", command=self.vet_clinic_finder, **btn_config).pack(pady=5)

        tk.Button(
            self,
            text="🔙 Back to Main Menu",
            font=("Segoe UI", 13, "bold"),
            bg="#7f8c8d",
            fg="white",
            activebackground="#616a6b",
            width=30,
            height=2,
            bd=0,
            command=self.back_to_menu
        ).pack(pady=(30, 20))

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