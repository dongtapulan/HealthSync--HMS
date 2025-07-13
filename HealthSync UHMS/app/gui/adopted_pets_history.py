import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk
from app.auth.user_manager import DB_PATH

class AdoptedPetsHistory(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#ecf0f1")
        self.master = master
        self.app = app
        self.username = username
        self.pack(fill="both", expand=True)

        self.build_ui()
        self.load_history()

    def build_ui(self):
        tk.Label(self, text="🐾 My Adopted Pets", font=("Segoe UI", 24, "bold"), bg="#ecf0f1", fg="#2c3e50").pack(pady=(20, 5))
        tk.Label(self, text="Here are the pets you've adopted:", font=("Segoe UI", 12), bg="#ecf0f1", fg="#7f8c8d").pack(pady=(0, 15))

        canvas = tk.Canvas(self, bg="#ecf0f1", highlightthickness=0)
        self.frame = tk.Frame(canvas, bg="#ecf0f1")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        tk.Button(self, text="🔙 Back", font=("Segoe UI", 11, "bold"), bg="#7f8c8d", fg="white",
                  command=self.back).pack(pady=(10,20))

    def load_history(self):
        for w in self.frame.winfo_children(): w.destroy()
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
                tk.Label(self.frame, text="You haven't adopted any pet yet.", font=("Segoe UI", 13),
                         bg="#ecf0f1", fg="#7f8c8d").pack(pady=30)
                return

            for name, species, breed, age, desc, date in recs:
                self._create_card(name, species, breed, age, desc, date)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load history.\n{e}")

    def _create_card(self, name, species, breed, age, desc, date):
        card = tk.Frame(self.frame, bg="white", bd=1, relief="solid")
        card.pack(padx=20, pady=10, fill="x")
        tk.Label(card, text=f"🐶 {name} — {species}, {breed}", font=("Segoe UI", 16, "bold"), bg="white").pack(anchor="w", padx=10, pady=(8,0))
        tk.Label(card, text=f"🎂 Age: {age} — 🗓️ Adopted on: {date}", font=("Segoe UI", 10), bg="white", fg="#7f8c8d").pack(anchor="w", padx=10)
        tk.Label(card, text=desc, font=("Segoe UI", 10), bg="white", wraplength=600, justify="left").pack(anchor="w", padx=10, pady=(5,8))

    def back(self):
        from app.gui.pet_dashboard import PetDashboard
        self.app._switch_frame(PetDashboard, self.app, self.username)
