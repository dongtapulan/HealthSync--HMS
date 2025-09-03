import tkinter as tk
from tkinter import messagebox
import sqlite3
from app.auth.user_manager import DB_PATH

class AdoptedPetsHistory(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#f4f6f7")
        self.master = master
        self.app = app
        self.username = username
        self.pack(fill="both", expand=True)

        self.build_ui()
        self.load_history()

    def build_ui(self):
        # Title Section
        tk.Label(
            self, text="🐾 My Adopted Pets",
            font=("Segoe UI", 18, "bold"),
            bg="#f4f6f7", fg="#2c3e50"
        ).pack(pady=(12, 2))

        tk.Label(
            self, text="A record of your adoption journey ❤️",
            font=("Segoe UI", 10),
            bg="#f4f6f7", fg="#7f8c8d"
        ).pack(pady=(0, 8))

        # Scrollable Frame
        container = tk.Frame(self, bg="#f4f6f7")
        container.pack(fill="both", expand=True, padx=10, pady=(0, 0))

        canvas = tk.Canvas(container, bg="#f4f6f7", highlightthickness=0)
        self.frame = tk.Frame(canvas, bg="#f4f6f7")
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Bottom Navigation (Back Button always visible)
        nav_frame = tk.Frame(self, bg="#f4f6f7")
        nav_frame.pack(fill="x", pady=(5, 10))

        tk.Button(
            nav_frame, text="🔙 Back to Pet Dashboard",
            font=("Segoe UI", 10, "bold"),
            bg="#7f8c8d", fg="white",
            activebackground="#616a6b",
            width=25, height=1, bd=0,
            command=self.back
        ).pack(pady=5)

    def load_history(self):
        for w in self.frame.winfo_children():
            w.destroy()

        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("""
                SELECT pet_name, species, breed, age, description, date_adopted
                FROM adopted_pets
                WHERE adopter_username = ?
                ORDER BY date_adopted DESC
            """, (self.username,))
            recs = c.fetchall()
            conn.close()

            if not recs:
                tk.Label(
                    self.frame, text="✨ You haven’t adopted any pet yet.",
                    font=("Segoe UI", 11), bg="#f4f6f7", fg="#7f8c8d"
                ).pack(pady=30)
                return

            for name, species, breed, age, desc, date in recs:
                self._create_card(name, species, breed, age, desc, date)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load history.\n{e}")

    def _create_card(self, name, species, breed, age, desc, date):
        card = tk.Frame(self.frame, bg="white", bd=1, relief="solid", padx=8, pady=6)
        card.pack(padx=12, pady=6, fill="x")

        # Pet Name + Species
        tk.Label(
            card, text=f"🐶 {name} ({species})",
            font=("Segoe UI", 13, "bold"),
            bg="white", fg="#2c3e50"
        ).pack(anchor="w")

        # Breed + Age + Adoption Date
        tk.Label(
            card, text=f"📖 Breed: {breed}   🎂 Age: {age}   🗓️ Adopted: {date}",
            font=("Segoe UI", 9), bg="white", fg="#7f8c8d"
        ).pack(anchor="w", pady=(2, 3))

        # Description
        tk.Label(
            card, text=desc,
            font=("Segoe UI", 9), bg="white", fg="#34495e",
            wraplength=550, justify="left"
        ).pack(anchor="w")

    def back(self):
        from app.gui.pet_dashboard import PetDashboard
        self.app._switch_frame(PetDashboard, self.app, self.username)
