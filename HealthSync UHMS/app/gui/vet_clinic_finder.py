import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim
import folium
import webbrowser
import os

def find_vet_clinics_near(location):
    # Create a map centered on the provided location
    geolocator = Nominatim(user_agent="pet_vet_locator")
    try:
        loc = geolocator.geocode(location)
        if not loc:
            raise ValueError("Location not found")
    except Exception as e:
        messagebox.showerror("Location Error", f"Error finding location: {e}")
        return

    map_obj = folium.Map(location=[loc.latitude, loc.longitude], zoom_start=14)

    # Simulate nearby vet clinics (you can replace these with real POIs if using APIs)
    clinics = [
        {"name": "Pawfect Vet Clinic", "lat": loc.latitude + 0.003, "lon": loc.longitude + 0.002},
        {"name": "Animal Wellness Center", "lat": loc.latitude - 0.002, "lon": loc.longitude + 0.003},
        {"name": "Happy Paws Veterinary", "lat": loc.latitude + 0.001, "lon": loc.longitude - 0.002},
    ]

    for clinic in clinics:
        folium.Marker(
            location=[clinic["lat"], clinic["lon"]],
            popup=clinic["name"],
            icon=folium.Icon(color='green', icon='plus-sign')
        ).add_to(map_obj)

    # Save and open map
    map_path = os.path.abspath("vet_clinic_map.html")
    map_obj.save(map_path)
    webbrowser.open(f"file://{map_path}")


class VetClinicFinder(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#f4f9fb")
        self.master = master
        self.app = app
        self.username = username
        self.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        tk.Label(
            self,
            text="📍 Find Nearby Vet Clinics",
            font=("Segoe UI", 20, "bold"),
            bg="#f4f9fb",
            fg="#2c3e50"
        ).pack(pady=(30, 10))

        tk.Label(
            self,
            text="Enter your city or area:",
            font=("Segoe UI", 12),
            bg="#f4f9fb"
        ).pack(pady=(10, 5))

        self.location_entry = tk.Entry(self, font=("Segoe UI", 12), width=40)
        self.location_entry.pack(pady=(0, 20))

        tk.Button(
            self,
            text="🔍 Search Vet Clinics",
            font=("Segoe UI", 12, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            width=30,
            height=2,
            bd=0,
            command=self.locate_clinics
        ).pack(pady=10)

        tk.Button(
            self,
            text="🔙 Back to Pet Dashboard",
            font=("Segoe UI", 11, "bold"),
            bg="#7f8c8d",
            fg="white",
            activebackground="#616a6b",
            width=25,
            height=2,
            bd=0,
            command=self.back_to_dashboard
        ).pack(pady=(20, 30))

    def locate_clinics(self):
        location = self.location_entry.get().strip()
        if not location:
            messagebox.showwarning("Missing Location", "Please enter your city or area.")
            return
        find_vet_clinics_near(location)

    def back_to_dashboard(self):
        from app.gui.pet_dashboard import PetDashboard
        self.app._switch_frame(PetDashboard, self.app, self.username)
