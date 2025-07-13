import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

from app.auth.user_manager import authenticate_user, DB_PATH
from app.auth.roles import ROLE_ADMIN, ROLE_PATIENT
from app.auth.auth_utils import hash_password


class LoginFrame(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master, bg="#e0f8ef")
        self.app = app
        self.master = master
        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        # Configure style
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", font=('Segoe UI', 11), background="#27ae60")
        style.configure("TEntry", padding=5)

        # Title
        tk.Label(
            self,
            text="HealthSync Unified Health Management System",
            font=("Segoe UI", 18, "bold"),
            bg="#2ecc71",
            fg="white",
            pady=10
        ).pack(fill="x", pady=(0, 20))

        # Container Frame
        container = tk.Frame(self, bg="white", bd=2, relief="ridge", highlightbackground="#1abc9c", highlightthickness=2)
        container.place(relx=0.5, rely=0.5, anchor="center", width=480, height=460)

        # Header
        tk.Label(container, text="🔒 Login to HealthSync", font=("Segoe UI", 18, "bold"), bg="white", fg="#34495e").pack(pady=20)

        # Username
        tk.Label(container, text="Username:", font=("Segoe UI", 12), bg="white", anchor="w").pack(fill="x", padx=40)
        self.username_entry = ttk.Entry(container, font=("Segoe UI", 11))
        self.username_entry.pack(pady=5, ipadx=5, ipady=4, padx=40, fill="x")

        # Password
        tk.Label(container, text="Password:", font=("Segoe UI", 12), bg="white", anchor="w").pack(fill="x", padx=40)
        self.password_entry = ttk.Entry(container, show="*", font=("Segoe UI", 11))
        self.password_entry.pack(pady=5, ipadx=5, ipady=4, padx=40, fill="x")

        # Login Button
        ttk.Button(container, text="Login", command=self.login).pack(pady=15, ipadx=10)

        # Register & Forgot Password
        button_frame = tk.Frame(container, bg="white")
        button_frame.pack(pady=(5, 10))

        tk.Button(
            button_frame,
            text="No account? Register here",
            font=("Segoe UI", 10, "underline"),
            fg="#2980b9",
            bg="white",
            bd=0,
            cursor="hand2",
            command=self.app.show_register
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Forgot password?",
            font=("Segoe UI", 10, "underline"),
            fg="red",
            bg="white",
            bd=0,
            cursor="hand2",
            command=self.forgot_password
        ).pack(side="right", padx=10)

        # Disclaimer
        tk.Label(
            self,
            text="⚠️ This system is for informational support only.\nPlease consult medical professionals for actual treatment.",
            font=("Segoe UI", 9, "italic"),
            bg="#e0f8ef",
            fg="#2c3e50",
            wraplength=460,
            justify="center"
        ).pack(pady=(20, 10))

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Input Error", "Please enter both username and password.")
            return

        role = authenticate_user(username, password)
        print(f"Login attempt: {username}, role: {role}")  # Debug

        if role:
            self.app.show_main_menu(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def forgot_password(self):
        win = tk.Toplevel(self)
        win.title("🔐 Forgot Password")
        win.geometry("400x350")
        win.configure(bg="white")

        tk.Label(win, text="Reset Your Password", font=("Segoe UI", 14, "bold"), bg="white", fg="#2c3e50").pack(pady=20)

        tk.Label(win, text="Enter your username:", font=("Segoe UI", 11), bg="white").pack()
        username_entry = ttk.Entry(win, font=("Segoe UI", 10))
        username_entry.pack(pady=5, ipadx=5, ipady=3)

        tk.Label(win, text="Enter new password:", font=("Segoe UI", 11), bg="white").pack()
        newpass_entry = ttk.Entry(win, font=("Segoe UI", 10), show="*")
        newpass_entry.pack(pady=5, ipadx=5, ipady=3)

        tk.Label(win, text="Confirm password:", font=("Segoe UI", 11), bg="white").pack()
        confirmpass_entry = ttk.Entry(win, font=("Segoe UI", 10), show="*")
        confirmpass_entry.pack(pady=5, ipadx=5, ipady=3)

        def reset():
            uname = username_entry.get().strip()
            newpass = newpass_entry.get().strip()
            confirmpass = confirmpass_entry.get().strip()

            if not uname or not newpass or not confirmpass:
                messagebox.showwarning("Input Error", "Please fill in all fields.")
                return

            if newpass != confirmpass:
                messagebox.showerror("Mismatch", "Passwords do not match.")
                return

            try:
                hashed_password = hash_password(newpass)
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (hashed_password, uname))
                if cursor.rowcount == 0:
                    messagebox.showerror("Error", "Username not found.")
                else:
                    conn.commit()
                    messagebox.showinfo("Success", "Password reset successful!")
                    win.destroy()
                conn.close()
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to reset password.\n\n{e}")

        tk.Button(win, text="🔁 Reset Password", bg="#27ae60", fg="white", font=("Segoe UI", 11, "bold"),
                  command=reset).pack(pady=20)
