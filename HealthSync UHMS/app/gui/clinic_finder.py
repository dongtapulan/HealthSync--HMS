import tkinter as tk
from tkinter import messagebox
import folium
import webbrowser
import os
from geopy.geocoders import Nominatim

class ClinicFinder(tk.Frame):
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
            text="📍 Nearby Clinic Finder",
            font=("Segoe UI", 20, "bold"),
            bg="#f4f9fb",
            fg="#2c3e50"
        ).pack(pady=(30, 10))

        # Instructions
        tk.Label(
            self,
            text="Search your city/location or click the button to view Cebu sample clinics:",
            font=("Segoe UI", 12),
            bg="#f4f9fb",
            fg="#34495e"
        ).pack(pady=(0, 10))

        # Search field
        self.search_entry = tk.Entry(self, font=("Segoe UI", 11), width=50)
        self.search_entry.pack(pady=5)

        tk.Button(
            self,
            text="🔍 Search and Show Map",
            font=("Segoe UI", 11, "bold"),
            bg="#2ecc71",
            fg="white",
            activebackground="#27ae60",
            width=25,
            height=2,
            bd=0,
            command=self.search_location
        ).pack(pady=(0, 10))

        # Default Cebu button
        tk.Button(
            self,
            text="🗺️ Show Cebu Clinics",
            font=("Segoe UI", 11, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            width=25,
            height=2,
            bd=0,
            command=self.generate_default_map
        ).pack(pady=10)

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
            command=self.back_to_dashboard
        ).pack(pady=(20, 30))

    def search_location(self):
        location_name = self.search_entry.get().strip()
        if not location_name:
            messagebox.showwarning("Missing Input", "Please enter a city or address.")
            return

        geolocator = Nominatim(user_agent="clinic_finder")
        location = geolocator.geocode(location_name)

        if location:
            lat, lon = location.latitude, location.longitude
            self.generate_map_with_marker(lat, lon, location_name)
        else:
            messagebox.showerror("Location Not Found", "Could not find the location. Try a more specific input.")

    def generate_map_with_marker(self, lat, lon, location_name):
        m = folium.Map(location=[lat, lon], zoom_start=14)
        folium.Marker(
            location=[lat, lon],
            popup=f"You searched: {location_name}",
            icon=folium.Icon(color="green", icon="search")
        ).add_to(m)

        map_path = "clinic_map_search.html"
        m.save(map_path)
        webbrowser.open('file://' + os.path.realpath(map_path))

    def generate_default_map(self):
        # Cebu City
        map_center = [10.3157, 123.8854]
        m = folium.Map(location=map_center, zoom_start=13)

        clinics = [
            {"name": "Cebu City Health Center", "location": [10.3111, 123.8917], "details": "Opens 8AM-5PM"},
            {"name": "Perpetual Succour Hospital", "location": [10.3123, 123.8995], "details": "Emergency 24/7"},
            {"name": "Chong Hua Hospital", "location": [10.3094, 123.8922], "details": "Cardio, OB-Gyne"},
            {"name": "Cebu Doctors' University Hospital", "location": [10.3176, 123.9022], "details": "General Hospital"},
        ]

        for clinic in clinics:
            popup_text = f"{clinic['name']}<br>{clinic['details']}"
            folium.Marker(
                location=clinic["location"],
                popup=popup_text,
                icon=folium.Icon(color="blue", icon="plus-sign")
            ).add_to(m)

        map_path = "clinic_map_cebu.html"
        m.save(map_path)
        webbrowser.open('file://' + os.path.realpath(map_path))

    def back_to_dashboard(self):
        from app.gui.patient_dashboard import PatientDashboard
        self.app._switch_frame(PatientDashboard, self.app, self.username)
