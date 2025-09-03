import tkinter as tk
from app.gui.login_window import LoginFrame
from app.gui.register_window import RegisterFrame
from app.gui.admin_dashboard import AdminDashboard
from app.gui.patient_dashboard import PatientDashboard
from app.gui.pet_dashboard import PetDashboard

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
            self._switch_frame(MainMenu, self, username)

    def _switch_frame(self, frame_class, *args):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = frame_class(self.root, *args)


class MainMenu(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#ecf0f1")
        self.master = master
        self.app = app
        self.username = username
        self.pack(fill="both", expand=True)

        # Top Header
        header = tk.Frame(self, bg="#2c3e50", height=60)
        header.pack(fill="x", side="top")

        tk.Label(
            header,
            text="🏥 HealthSync - Main Menu",
            font=("Segoe UI", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(side="left", padx=20, pady=10)

        # Welcome Message
        tk.Label(
            self,
            text=f"Welcome, {username}! ✨",
            font=("Segoe UI", 20, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        ).pack(pady=(40, 20))

        # Center Frame (Card style)
        card = tk.Frame(self, bg="white", bd=2, relief="ridge")
        card.pack(pady=10, ipadx=30, ipady=30)

        # Human Support Button
        self.create_button(
            card,
            "🧍 Human Health Support",
            "#3498db",
            "#2980b9",
            self.launch_human
        ).pack(pady=15)

        # Pet Support Button
        self.create_button(
            card,
            "🐶 Pet Health Support",
            "#2ecc71",
            "#27ae60",
            self.launch_pet
        ).pack(pady=15)

        # Back Button
        self.create_button(
            self,
            "⏪ Back to Login",
            "#7f8c8d",
            "#616a6b",
            self.back_to_login,
            font_size=11,
            width=22
        ).pack(pady=(40, 10))

    # Reusable styled button
    def create_button(self, parent, text, bg, hover_bg, command, font_size=13, width=28):
        btn = tk.Button(
            parent,
            text=text,
            font=("Segoe UI", font_size, "bold"),
            bg=bg,
            fg="white",
            width=width,
            height=2,
            bd=0,
            relief="flat",
            command=command
        )

        # Hover effect
        def on_enter(e): btn.config(bg=hover_bg)
        def on_leave(e): btn.config(bg=bg)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        return btn

    def launch_human(self):
        self.app._switch_frame(PatientDashboard, self.app, self.username)

    def launch_pet(self):
        self.app._switch_frame(PetDashboard, self.app, self.username)

    def back_to_login(self):
        self.app.show_login()
