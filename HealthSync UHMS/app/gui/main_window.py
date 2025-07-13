import tkinter as tk
from app.gui.login_window import LoginFrame
from app.gui.register_window import RegisterFrame
from app.gui.admin_dashboard import AdminDashboard
from app.gui.patient_dashboard import PatientDashboard  # <-- Add this import
from app.gui.pet_dashboard import PetDashboard  # <-- Add this import at the top

class HealthSyncApp:
    def __init__(self, root):
        self.root = root
        self.current_frame = None
        self.show_login()

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()

    def show_login(self):
        self.clear_frame()
        self.current_frame = LoginFrame(self.root, self)

    def show_register(self):
        self.clear_frame()
        self.current_frame = RegisterFrame(self.root, self)

    def show_main_menu(self, username):
        import sqlite3
        conn = sqlite3.connect("app/data/patients.db")
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        role = result[0] if result else None

        if role == "admin":
            self._switch_frame(AdminDashboard, username)
        else:
            self._switch_frame(MainMenu, self, username)  # Pass self as app

    def _switch_frame(self, frame_class, *args):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self.root, *args)

class MainMenu(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#f0fff9")  # Light blue background
        self.master = master
        self.app = app
        self.username = username
        self.pack(fill="both", expand=True)

        # Welcome text
        tk.Label(
            self,
            text=f"Welcome, {username}!",
            font=("Segoe UI", 22, "bold"),
            bg="#f0f8ff",
            fg="#2c3e50"
        ).pack(pady=30)

        # Human Support Button - Blue
        self.human_btn = tk.Button(
            self,
            text="🧍 Human Health Support",
            font=("Segoe UI", 14, "bold"),
            bg="#3498db",   # Blue
            fg="white",
            width=28,
            height=2,
            bd=0,
            activebackground="#2980b9",
            command=self.launch_human
        )
        self.human_btn.pack(pady=15)

        # Pet Support Button - Green
        self.pet_btn = tk.Button(
            self,
            text="🐶 Pet Health Support",
            font=("Segoe UI", 14, "bold"),
            bg="#2ecc71",   # Green
            fg="white",
            width=28,
            height=2,
            bd=0,
            activebackground="#27ae60",
            command=self.launch_pet
        )
        self.pet_btn.pack(pady=15)

        # Back to Login Button - Gray
        self.back_btn = tk.Button(
            self,
            text="⏪ Back to Login",
            font=("Segoe UI", 12, "bold"),
            bg="#7f8c8d",
            fg="white",
            width=20,
            height=2,
            bd=0,
            activebackground="#616a6b",
            command=self.back_to_login
        )
        self.back_btn.pack(pady=(40, 10))

    def launch_human(self):
        self.app._switch_frame(PatientDashboard, self.app, self.username)  # Switch to PatientDashboard

    def launch_pet(self):
        self.app._switch_frame(PetDashboard, self.app, self.username)  # Switch to PetDashboard

    def back_to_login(self):
        self.app.show_login()