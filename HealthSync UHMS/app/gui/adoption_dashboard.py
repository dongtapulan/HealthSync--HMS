import tkinter as tk
from tkinter import messagebox, PhotoImage
import sqlite3
from datetime import datetime
from PIL import Image, ImageTk
from app.auth.user_manager import DB_PATH

class AdoptionDashboard(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#ecf0f1")
        self.master = master
        self.app = app
        self.username = username
        self.pack(fill="both", expand=True)

        self.ensure_adopted_table()
        self.build_ui()
        self.load_adoptions()

    # Inside AdoptionDashboard class, add this in ensure_adopted_table()
    def ensure_adopted_table(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS adopted_pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pet_name TEXT NOT NULL,
                species TEXT,
                breed TEXT,
                age INTEGER,
                description TEXT,
                owner_username TEXT,
                adopter_username TEXT,
                date_adopted TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS adoption_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pet_name TEXT,
                owner_username TEXT,
                sender_username TEXT,
                message TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()
        conn.close()

    def build_ui(self):
        tk.Label(
            self,
            text="🐾 Pet Adoption Center",
            font=("Segoe UI", 24, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        ).pack(pady=(20, 5))

        tk.Label(
            self,
            text="Adopt a lovely companion today!",
            font=("Segoe UI", 12),
            bg="#ecf0f1",
            fg="#7f8c8d"
        ).pack(pady=(0, 15))
        
        tk.Button(
            self,
            text="📬 Chat Inbox",
            font=("Segoe UI", 10, "bold"),
            bg="#2ecc71",
            fg="white",
            command=self.open_chat_inbox
        ).pack(pady=5)


        # Scrollable Frame Setup
        canvas = tk.Canvas(self, bg="#ecf0f1", highlightthickness=0)
        self.scrollable_frame = tk.Frame(canvas, bg="#ecf0f1")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Refresh Button
        tk.Button(
            self,
            text="🔄 Refresh Listings",
            font=("Segoe UI", 10, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            width=20,
            command=self.load_adoptions
        ).pack(pady=(10, 0))

        # Back to dashboard
        tk.Button(
            self,
            text="🔙 Back to Dashboard",
            font=("Segoe UI", 11, "bold"),
            bg="#7f8c8d",
            fg="white",
            activebackground="#616a6b",
            width=25,
            height=2,
            bd=0,
            command=self.back_to_pet_dashboard
        ).pack(pady=(20, 30))

    def load_adoptions(self):
        # Clear previous cards
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Exclude already adopted pets
            cursor.execute("""
                SELECT a.id, a.owner_username, a.pet_name, a.species, a.breed, a.age, a.description, p.image_path
                FROM adoption_list a
                LEFT JOIN adopted_pets ad ON a.pet_name = ad.pet_name AND a.owner_username = ad.owner_username
                LEFT JOIN pets p ON p.pet_name = a.pet_name AND p.owner_username = a.owner_username
                WHERE ad.id IS NULL
            """)
            records = cursor.fetchall()
            conn.close()

            if not records:
                tk.Label(
                    self.scrollable_frame,
                    text="😿 No pets listed for adoption at the moment.",
                    font=("Segoe UI", 13),
                    bg="#ecf0f1",
                    fg="#7f8c8d"
                ).pack(pady=30)
                return

            for record in records:
                self.create_pet_card(*record)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load adoption data.\n{e}")

    def create_pet_card(self, adoption_id, owner, name, species, breed, age, description, image_path):
        card = tk.Frame(self.scrollable_frame, bg="white", bd=1, relief="solid")
        card.pack(padx=20, pady=10, fill="x", expand=True)

        container = tk.Frame(card, bg="white")
        container.pack(fill="x", padx=15, pady=10)

    # Pet Image (thumbnail)
        if image_path:
            try:
                image = Image.open(image_path)
                image.thumbnail((100, 100))
                photo = ImageTk.PhotoImage(image)
                img_label = tk.Label(container, image=photo, bg="white")
                img_label.image = photo  # Keep reference
                img_label.pack(side="left", padx=(0, 15))
            except Exception:
                tk.Label(container, text="No Image", bg="gray", fg="white", width=12, height=6).pack(side="left", padx=(0, 15))
        else:
            tk.Label(container, text="No Image", bg="gray", fg="white", width=12, height=6).pack(side="left", padx=(0, 15))

        # Pet Details
        details = tk.Frame(container, bg="white")
        details.pack(side="left", fill="both", expand=True)

        tk.Label(details, text=f"🐶 {name}", font=("Segoe UI", 16, "bold"), bg="white", anchor="w").pack(anchor="w")
        tk.Label(details, text=f"🧬 {species} – {breed} | 🎂 Age: {age}", font=("Segoe UI", 11), bg="white", fg="#34495e", anchor="w").pack(anchor="w")
        tk.Label(details, text=f"📄 {description}", font=("Segoe UI", 10), bg="white", wraplength=600, justify="left", anchor="w").pack(anchor="w", pady=(5, 0))
        tk.Label(details, text=f"👤 Owner: {owner}", font=("Segoe UI", 9, "italic"), fg="#7f8c8d", bg="white", anchor="w").pack(anchor="w", pady=(0, 5))

        # Adopt Button
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(pady=(0, 10))

        tk.Button(
            btn_frame,
            text="❤️ Adopt",
            font=("Segoe UI", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            width=15,
            command=lambda: self.confirm_adoption(owner, name, species, breed, age, description)
        ).pack(side="left", padx=5)

        # 💬 Chat Button
        tk.Button(
            btn_frame,
            text="💬 Chat with Owner",
            font=("Segoe UI", 10, "bold"),
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            width=18,
            command=lambda: self.open_chat_window(name, owner)
        ).pack(side="left", padx=5)


    def confirm_adoption(self, owner, name, species, breed, age, description):
        if owner == self.username:
            messagebox.showwarning("Adoption Not Allowed", "You can't adopt your own pet!")
            return

        if messagebox.askyesno("Confirm Adoption", f"Do you want to adopt {name}?"):
            try:
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO adopted_pets (pet_name, species, breed, age, description, owner_username, adopter_username, date_adopted)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    name, species, breed, age, description, owner, self.username, datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ))
                conn.commit()
                conn.close()

                messagebox.showinfo("Adoption Confirmed", f"🎉 You have adopted {name}!")
                self.load_adoptions()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to process adoption.\n{e}")    
                    

    def send_message(self, pet_name, owner_username, input_field, display):
        msg = input_field.get().strip()
        if not msg: return
        input_field.delete(0, "end")
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO adoption_messages (pet_name, owner_username, sender_username, message, timestamp)
            VALUES (?, ?, ?, ?, ?)
            """, (pet_name, owner_username, self.username, msg, now))
            conn.commit()
            conn.close()

            display.config(state="normal")
            display.insert("end", f"[{now}] {self.username}: {msg}\n")
            display.config(state="disabled")
            display.see("end")
        except Exception as e:
            messagebox.showerror("Send Failed", f"Could not send message.\n{e}")
    
    def open_chat_window(self, pet_name, owner_username):
        win = tk.Toplevel(self)
        win.title(f"Chat about {pet_name}")
        win.geometry("450x500")
        win.configure(bg="#f9f9f9")

        chat_frame = tk.Frame(win, bg="white")
        chat_frame.pack(fill="both", expand=True, padx=10, pady=10)

        chat_display = tk.Text(chat_frame, wrap="word", font=("Segoe UI", 10), state="disabled", bg="#fefefe")
        chat_display.pack(fill="both", expand=True)

        input_frame = tk.Frame(win)
        input_frame.pack(fill="x", padx=10, pady=5)
        input_field = tk.Entry(input_frame, font=("Segoe UI", 10))
        input_field.pack(side="left", fill="x", expand=True, padx=(0, 5))
        send_btn = tk.Button(input_frame, text="Send", bg="#27ae60", fg="white",
                         command=lambda: self.send_message(pet_name, owner_username, input_field, chat_display))
        send_btn.pack(side="right")

        # Load previous messages
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT sender_username, message, timestamp FROM adoption_messages
                WHERE pet_name = ? AND owner_username = ?
                ORDER BY timestamp ASC
            """, (pet_name, owner_username))
            messages = cursor.fetchall()
            conn.close()

            chat_display.config(state="normal")
            for sender, msg, ts in messages:
                chat_display.insert("end", f"[{ts}] {sender}: {msg}\n")
            chat_display.config(state="disabled")
            chat_display.see("end")

        except Exception as e:
            messagebox.showerror("Chat Error", f"Couldn't load messages.\n{e}")

    def open_chat_inbox(self):
        win = tk.Toplevel(self)
        win.title("📬 Adoption Inbox")
        win.geometry("500x600")
        win.configure(bg="#f4f4f4")

        # ✅ Define listbox as a local variable
        inbox_listbox = tk.Listbox(win, font=("Segoe UI", 11))
        inbox_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT pet_name, sender_username
                FROM adoption_messages
                WHERE owner_username = ?
                ORDER BY timestamp DESC
            """, (self.username,))
            chats = cursor.fetchall()
            conn.close()

            for pet_name, sender in chats:
                inbox_listbox.insert("end", f"🐾 {pet_name} – From: {sender}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load messages.\n{e}")
            return

    # ✅ on_select is nested and uses inbox_listbox from parent scope
        def on_select(event):
            selection = inbox_listbox.curselection()
            if not selection:
                return  # Nothing selected

            selected_text = inbox_listbox.get(selection[0])
            try:
                pet, sender = selected_text.split(" – From: ")
                self.open_chat_window(pet.replace("🐾 ", ""), self.username)
            except ValueError:
                messagebox.showerror("Error", "Invalid message format.")

        inbox_listbox.bind("<<ListboxSelect>>", on_select)

    def back_to_pet_dashboard(self):
        from app.gui.pet_dashboard import PetDashboard
        self.app._switch_frame(PetDashboard, self.app, self.username)
