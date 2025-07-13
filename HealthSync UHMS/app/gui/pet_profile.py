import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import sqlite3
from app.auth.user_manager import DB_PATH

class PetProfile(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#f4f9fb")
        self.master = master
        self.app = app
        self.username = username
        self.pet_image_path = None
        self.pack(fill="both", expand=True)

        self.build_ui()
        self.load_pets()

    def build_ui(self):
        # Title
        tk.Label(
            self,
            text=f"🐾 Pet Profiles – {self.username}",
            font=("Segoe UI", 22, "bold"),
            bg="#f4f9fb",
            fg="#2c3e50"
        ).pack(pady=20)

        # Form Frame
        form_frame = tk.Frame(self, bg="#f4f9fb")
        form_frame.pack(pady=10)

        # Entry Style
        entry_style = {"bg": "white", "relief": "flat", "font": ("Segoe UI", 11), "width": 25}

        # Labels and Entries
        fields = [("Name", "name_entry"), ("Species", "species_entry"), ("Breed", "breed_entry"),
                  ("Age", "age_entry"), ("Description", "desc_entry")]

        for i, (label, attr) in enumerate(fields):
            tk.Label(form_frame, text=label + ":", bg="#f4f9fb", font=("Segoe UI", 11)).grid(row=i, column=0, sticky="e", pady=4, padx=5)
            entry = tk.Entry(form_frame, **entry_style)
            setattr(self, attr, entry)
            entry.grid(row=i, column=1, pady=4, padx=5)

        # Image Upload & Preview Column
        image_frame = tk.Frame(form_frame, bg="#f4f9fb")
        image_frame.grid(row=0, column=2, rowspan=5, padx=15, sticky="n")

        # Fixed-size preview area
        self.img_frame = tk.Frame(image_frame, width=140, height=140, bg="white", relief="groove", bd=1)
        self.img_frame.pack(pady=5)
        self.img_frame.pack_propagate(False)

        self.img_label = tk.Label(self.img_frame, text="No Image", bg="white", fg="gray")
        self.img_label.pack(expand=True)

        # Upload Button
        tk.Button(
            image_frame, text="📁 Upload Image", font=("Segoe UI", 9, "bold"),
            bg="#2980b9", fg="white", relief="flat", width=18,
            command=self.upload_image
        ).pack(pady=(10, 0))

        # Add Pet Button
        tk.Button(
            form_frame, text="➕ Add Pet", font=("Segoe UI", 11, "bold"),
            bg="#2ecc71", fg="white", relief="flat",
            width=20, command=self.add_pet
        ).grid(row=5, column=1, pady=12)

        # --- Pet List ---
        list_frame = tk.Frame(self, bg="#f4f9fb")
        list_frame.pack(pady=20, fill="x")

        tk.Label(
            list_frame, text="📋 Your Pets:", font=("Segoe UI", 13, "bold"),
            bg="#f4f9fb", fg="#2c3e50"
        ).pack(anchor="w", padx=10)

        self.pet_listbox = tk.Listbox(list_frame, width=60, height=6, font=("Segoe UI", 10))
        self.pet_listbox.pack(side="left", padx=10, pady=5)
        self.pet_listbox.bind("<<ListboxSelect>>", self.on_pet_select)

        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=self.pet_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.pet_listbox.config(yscrollcommand=scrollbar.set)

        # Adoption Button
        tk.Button(
            self, text="📤 Post Selected Pet for Adoption",
            font=("Segoe UI", 11, "bold"),
            bg="#3498db", fg="white", relief="flat", width=35,
            command=self.post_for_adoption
        ).pack(pady=10)

        # Back Button
        tk.Button(
            self,
            text="🔙 Back to Pet Dashboard",
            font=("Segoe UI", 11, "bold"),
            bg="#7f8c8d", fg="white", relief="flat",
            width=25, height=2,
            command=self.back_to_dashboard
        ).pack(pady=20)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Pet Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")]
        )
        if file_path:
            self.pet_image_path = file_path
            img = Image.open(file_path)
            img = ImageOps.contain(img, (140, 140))  # Resize to fit frame
            self.img = ImageTk.PhotoImage(img)
            self.img_label.config(image=self.img, text="")  # Show image
        else:
            self.pet_image_path = None
            self.img_label.config(image="", text="No Image")  # Reset preview

    def add_pet(self):
        name = self.name_entry.get().strip()
        species = self.species_entry.get().strip()
        breed = self.breed_entry.get().strip()
        age = self.age_entry.get().strip()
        desc = self.desc_entry.get().strip()
        img_path = self.pet_image_path

        if not name or not species:
            messagebox.showwarning("Input Error", "Name and Species are required.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_username TEXT NOT NULL,
                pet_name TEXT NOT NULL,
                species TEXT NOT NULL,
                breed TEXT,
                age INTEGER,
                description TEXT,
                image_path TEXT
            )
        """)
        cursor.execute(
            "INSERT INTO pets (owner_username, pet_name, species, breed, age, description, image_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (self.username, name, species, breed, age, desc, img_path)
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "✅ Pet added successfully!")
        self.clear_form()
        self.load_pets()

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.species_entry.delete(0, tk.END)
        self.breed_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.pet_image_path = None
        self.img_label.config(image="", text="No Image")

    def load_pets(self):
        self.pet_listbox.delete(0, tk.END)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, pet_name, species, breed, age FROM pets WHERE owner_username = ?", (self.username,))
        self.pets = cursor.fetchall()
        for pet in self.pets:
            pet_id, name, species, breed, age = pet
            self.pet_listbox.insert(tk.END, f"{name} ({species}, {breed}, Age: {age})")
        conn.close()

    def on_pet_select(self, event):
        pass  # Future: show pet preview

    def post_for_adoption(self):
        selection = self.pet_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a pet to post for adoption.")
            return
        index = selection[0]
        pet = self.pets[index]
        pet_id, name, species, breed, age = pet

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT description FROM pets WHERE id = ?", (pet_id,))
        desc_row = cursor.fetchone()
        description = desc_row[0] if desc_row else ""

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS adoption_list (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_username TEXT,
                pet_name TEXT,
                species TEXT,
                breed TEXT,
                age INTEGER,
                description TEXT
            )
        """)
        cursor.execute(
            "INSERT INTO adoption_list (owner_username, pet_name, species, breed, age, description) VALUES (?, ?, ?, ?, ?, ?)",
            (self.username, name, species, breed, age, description)
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Adoption Posted", f"🐾 '{name}' is now listed for adoption!")

    def back_to_dashboard(self):
        from app.gui.pet_dashboard import PetDashboard
        self.app._switch_frame(PetDashboard, self.app, self.username)
