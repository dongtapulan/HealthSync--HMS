import tkinter as tk
from tkinter import ttk, messagebox
from app.auth.user_manager import register_user, user_exists
from app.auth.roles import ROLE_PATIENT

class RegisterFrame(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg="#f0f8ff")  # Subtle background
        self.app = app
        self.master = master
        self.pack(fill="both", expand=True)

        self.build_ui()

    def build_ui(self):
        # Centered container
        container = tk.Frame(self, bg="white", bd=2, relief="groove")
        container.place(relx=0.5, rely=0.5, anchor="center", width=480, height=420)

        # Title
        tk.Label(
            container,
            text="📝 Register New Account",
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=(30, 18))

        # Username
        tk.Label(
            container,
            text="Username:",
            font=("Segoe UI", 13),
            bg="white"
        ).pack(anchor="w", padx=40)
        self.username_entry = ttk.Entry(container, font=("Segoe UI", 12))
        self.username_entry.pack(pady=8, padx=40, fill="x")

        # Password
        tk.Label(
            container,
            text="Password:",
            font=("Segoe UI", 13),
            bg="white"
        ).pack(anchor="w", padx=40)
        self.password_entry = ttk.Entry(container, show="*", font=("Segoe UI", 12))
        self.password_entry.pack(pady=8, padx=40, fill="x")

        # Register button
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Segoe UI", 13, "bold"), foreground="blue", background="#0078d7")
        register_btn = ttk.Button(
            container,
            text="Register",
            style="Accent.TButton",
            command=self.register
        )
        register_btn.pack(pady=(25, 10), ipadx=10, ipady=4)

        # Back to Login link
        tk.Button(
            container,
            text="← Back to Login",
            font=("Segoe UI", 11, "underline"),
            fg="#0078d7",
            bg="white",
            bd=0,
            cursor="hand2",
            command=self.app.show_login,
            activeforeground="#005fa3"
        ).pack()

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        if user_exists(username):
            messagebox.showwarning("User Exists", "Username already taken.")
        else:
            success = register_user(username, password, role=ROLE_PATIENT)
            if success:
                messagebox.showinfo("Success", "Registration successful!")
                self.app.show_login()
            else:
                messagebox.showerror("Error", "Failed to register user.")
