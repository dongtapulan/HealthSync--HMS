import tkinter as tk
from tkinter import ttk, messagebox
from collections import Counter
from datetime import datetime
from app.database import db_manager
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os


class HealthSummaryView(tk.Frame):
    def __init__(self, master, app, username):
        super().__init__(master, bg="#f4f9fb")
        self.master = master
        self.app = app
        self.username = username
        self.pack(fill="both", expand=True)
        self.build_ui()
        self.load_summary()

    def build_ui(self):
        tk.Label(
            self,
            text=f"📊 Health Summary for {self.username}",
            font=("Segoe UI", 18, "bold"),
            bg="#f4f9fb",
            fg="#2c3e50"
        ).pack(pady=(20, 10))

        self.summary_text = tk.Text(self, height=12, width=70, font=("Segoe UI", 10), wrap="word", bg="white")
        self.summary_text.pack(padx=20, pady=10)

        self.chart_frame = tk.Frame(self, bg="#f4f9fb")
        self.chart_frame.pack(pady=(0, 10))

        button_frame = tk.Frame(self, bg="#f4f9fb")
        button_frame.pack()

        tk.Button(
            button_frame,
            text="📤 Export Health Report (PDF)",
            font=("Segoe UI", 10, "bold"),
            bg="#1abc9c",
            fg="white",
            activebackground="#16a085",
            width=30,
            height=2,
            bd=0,
            command=self.export_pdf
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_frame,
            text="🔙 Back to Dashboard",
            font=("Segoe UI", 11, "bold"),
            bg="#7f8c8d",
            fg="white",
            activebackground="#616a6b",
            width=25,
            height=2,
            bd=0,
            command=self.back_to_dashboard
        ).grid(row=0, column=1, padx=10)

    def load_summary(self):
        conn = db_manager.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT date, symptoms, diagnosis FROM diagnosis_history WHERE username = ?", (self.username,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            self.summary_text.insert(tk.END, "No checkup history found.")
            return

        self.diagnoses = [row[2] for row in rows]
        self.symptoms = [s.strip() for row in rows for s in row[1].split(",")]
        self.dates = [row[0] for row in rows]
        total = len(rows)

        most_recent = self.dates[-1] if self.dates else "N/A"
        top_diagnosis = Counter(self.diagnoses).most_common(1)
        top_symptoms = Counter(self.symptoms).most_common(5)

        summary = (
            f"📝 Total Checkups: {total}\n"
            f"📆 Most Recent Checkup: {most_recent}\n\n"
            f"🏥 Most Frequent Diagnosis:\n"
            f"   → {top_diagnosis[0][0]} ({top_diagnosis[0][1]} times)\n\n"
            f"😷 Common Symptoms:\n"
        )
        for sym, count in top_symptoms:
            summary += f"   • {sym} ({count} times)\n"

        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, summary)

        self.render_chart()

    def render_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        counts = Counter(self.diagnoses).most_common(5)
        if not counts:
            return

        labels, values = zip(*counts)

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.barh(labels, values, color="#3498db")
        ax.set_title("Top Diagnoses")
        ax.set_xlabel("Frequency")
        ax.invert_yaxis()
        fig.tight_layout()

        self.chart_path = f"chart_{self.username}.png"
        fig.savefig(self.chart_path)
        plt.close(fig)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def export_pdf(self):
        try:
            from PIL import Image

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_path = f"health_report_{self.username}_{timestamp}.pdf"
            c = canvas.Canvas(file_path, pagesize=A4)
            width, height = A4
            margin = 50
            y = height - margin

            c.setFont("Helvetica-Bold", 16)
            c.drawString(margin, y, f"🩺 Health Summary Report for {self.username}")
            y -= 30

            # Optional Profile Image
            profile_img_path = f"profile_images/{self.username}.png"
            if os.path.exists(profile_img_path):
                c.drawImage(profile_img_path, width - 120, height - 130, width=70, height=70)

            # Summary Text
            c.setFont("Helvetica", 10)
            for line in self.summary_text.get("1.0", tk.END).splitlines():
                if line.strip():
                    c.drawString(margin, y, line.strip())
                    y -= 15
                if y < 120:
                    c.showPage()
                    y = height - margin

            # Chart Image
            if os.path.exists(self.chart_path):
                if y < 250:
                    c.showPage()
                    y = height - margin
                c.drawImage(self.chart_path, margin, y - 200, width=400, height=200)
                y -= 220

            # Disclaimer
            if y < 100:
                c.showPage()
                y = height - margin
            c.setFont("Helvetica-Oblique", 8)
            c.setFillColorRGB(0.3, 0.3, 0.3)
            c.drawString(margin, y, "*Note: This health report is for informational purposes only and does not replace professional medical advice.")

            c.save()

            # Cleanup
            if os.path.exists(self.chart_path):
                os.remove(self.chart_path)

            messagebox.showinfo("PDF Exported", f"PDF saved as:\n{os.path.abspath(file_path)}")

        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not export PDF:\n{e}")

    def back_to_dashboard(self):
        from app.gui.patient_dashboard import PatientDashboard
        self.app._switch_frame(PatientDashboard, self.app, self.username)
    
def export_latest_health_pdf(username):
    import matplotlib.pyplot as plt
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from collections import Counter
    from datetime import datetime
    import os
    from app.database import db_manager

    conn = db_manager.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT date, symptoms, diagnosis FROM diagnosis_history WHERE username = ?", (username,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        raise Exception("No checkup history found.")

    diagnoses = [row[2] for row in rows]
    symptoms = [s.strip() for row in rows for s in row[1].split(",")]
    dates = [row[0] for row in rows]
    total = len(rows)

    most_recent = dates[-1] if dates else "N/A"
    top_diagnosis = Counter(diagnoses).most_common(1)
    top_symptoms = Counter(symptoms).most_common(5)

    summary = [
        f"📝 Total Checkups: {total}",
        f"📆 Most Recent Checkup: {most_recent}",
        "",
        f"🏥 Most Frequent Diagnosis: {top_diagnosis[0][0]} ({top_diagnosis[0][1]} times)",
        "",
        "😷 Common Symptoms:"
    ]
    for sym, count in top_symptoms:
        summary.append(f"• {sym} ({count} times)")

    # Chart: Save as PNG
    chart_path = f"chart_{username}.png"
    counts = Counter(diagnoses).most_common(5)
    if counts:
        labels, values = zip(*counts)
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.barh(labels, values, color="#3498db")
        ax.set_title("Top Diagnoses")
        ax.set_xlabel("Frequency")
        ax.invert_yaxis()
        fig.tight_layout()
        fig.savefig(chart_path)
        plt.close(fig)

    # Export PDF
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_path = f"health_report_{username}_{timestamp}.pdf"
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    margin = 50
    y = height - margin

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, y, f"🩺 Health Summary Report for {username}")
    y -= 30

    # Text Summary
    c.setFont("Helvetica", 10)
    for line in summary:
        c.drawString(margin, y, line)
        y -= 15
        if y < 100:
            c.showPage()
            y = height - margin

    # Include Chart
    if os.path.exists(chart_path):
        if y < 250:
            c.showPage()
            y = height - margin
        c.drawImage(chart_path, margin, y - 220, width=400, height=200)
        os.remove(chart_path)

    # Disclaimer
    c.setFont("Helvetica-Oblique", 8)
    c.setFillColorRGB(0.3, 0.3, 0.3)
    c.drawString(margin, 40, "*This document is generated for informational purposes and is not a substitute for medical advice from licensed professionals.")

    c.save()
