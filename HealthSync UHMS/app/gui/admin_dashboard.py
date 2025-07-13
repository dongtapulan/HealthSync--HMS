import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
from app.auth.user_manager import DB_PATH
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AdminDashboard(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master, bg="white")
        self.master = master
        self.username = username
        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        tk.Label(
            self,
            text=f"👨‍⚕️ Welcome, Admin {self.username}",
            font=("Segoe UI", 20, "bold"),
            bg="white",
            fg="#2c3e50"
        ).pack(pady=20)

        tk.Button(self, text="📋 View All Patients", font=("Segoe UI", 12), width=25, command=self.view_all_patients).pack(pady=10)
        tk.Button(self, text="🐶 View All Pets", font=("Segoe UI", 12), width=25, command=self.view_all_pets).pack(pady=10)
        tk.Button(self, text="📈 Health Statistics", font=("Segoe UI", 12), width=25, command=self.show_statistics).pack(pady=10)
        tk.Button(self, text="🔐 Manage Users", font=("Segoe UI", 12), width=25, command=self.manage_users).pack(pady=10)
        tk.Button(self, text="🚪 Logout", font=("Segoe UI", 12), width=25, command=self.logout).pack(pady=30)

    def logout(self):
        from app.gui.main_window import HealthSyncApp
        self.destroy()
        app = HealthSyncApp(self.master)
        app.show_login()

    def view_all_patients(self):
        query = "SELECT username FROM users WHERE username != 'admin'"
        self._open_table_window("All Registered Users", query, ["Username"])

    def view_all_pets(self):
        query = "SELECT pet_name, breed, description, age, owner_username FROM pets"
        self._open_table_window("All Pets", query, ["Name", "Breed", "Description", "Age", "Owner"])

    def manage_users(self):
        win = tk.Toplevel(self)
        win.title("Manage Users")
        win.geometry("600x400")
        win.configure(bg="white")

        tree = ttk.Treeview(win, columns=("Username",), show="headings")
        tree.heading("Username", text="Username")
        tree.pack(fill="both", expand=True)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username != 'admin'")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

        def delete_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showinfo("No selection", "Please select a user to delete.")
                return
            user = tree.item(selected[0])["values"][0]
            if messagebox.askyesno("Delete?", f"Are you sure you want to delete user: {user}?"):
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE username=?", (user,))
                conn.commit()
                conn.close()
                tree.delete(selected[0])
                messagebox.showinfo("Deleted", f"User {user} has been deleted.")

        tk.Button(win, text="Delete Selected User", bg="red", fg="white", command=delete_selected).pack(pady=10)

    def show_statistics(self):
        win = tk.Toplevel(self)
        win.title("📊 Health Statistics")
        win.geometry("600x500")
        win.configure(bg="white")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Raw stats
        cursor.execute("SELECT COUNT(*) FROM users WHERE username != 'admin'")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM pets")
        total_pets = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM adopted_pets")
        total_adopted = cursor.fetchone()[0]

        # For line chart: count adoptions per day
        cursor.execute("""
            SELECT DATE(date_adopted), COUNT(*) 
            FROM adopted_pets 
            GROUP BY DATE(date_adopted) 
            ORDER BY DATE(date_adopted) ASC
        """)
        rows = cursor.fetchall()
        conn.close()

        tk.Label(win, text=f"Total Registered Patients: {total_users}", font=("Segoe UI", 12), bg="white").pack(pady=5)
        tk.Label(win, text=f"Total Pets in System: {total_pets}", font=("Segoe UI", 12), bg="white").pack(pady=5)
        tk.Label(win, text=f"Total Pets Adopted: {total_adopted}", font=("Segoe UI", 12), bg="white").pack(pady=5)

        # 📈 Chart
        if rows:
            dates = [row[0] for row in rows]
            counts = [row[1] for row in rows]

            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(dates, counts, marker="o", linestyle="-", color="#27ae60")
            ax.set_title("Adoptions Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel("Number of Adoptions")
            ax.grid(True)

            chart = FigureCanvasTkAgg(fig, win)
            chart.get_tk_widget().pack(pady=10)
            chart.draw()
        else:
            tk.Label(win, text="No adoption records yet.", bg="white", fg="gray").pack(pady=20)

    def _open_table_window(self, title, query, columns):
        win = tk.Toplevel(self)
        win.title(title)
        win.geometry("600x500")
        win.configure(bg="white")

        tree = ttk.Treeview(win, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill="both", expand=True)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
        conn.close()
