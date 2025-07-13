from tkinter import Tk, Frame, Label, PhotoImage, ttk
from app.gui.main_window import HealthSyncApp
from app.database import db_manager
import os
import time

class SplashScreen:
    def __init__(self):
        self.splash = Tk()
        self.splash.overrideredirect(True)
        self._center_window(500, 300)
        self.splash.attributes('-alpha', 0.0)
        self.splash.configure(bg='#ffffff')
        self._setup_ui()
        
    def _center_window(self, width, height):
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.splash.geometry(f"{width}x{height}+{x}+{y}")
        
    def _setup_ui(self):
        # Logo with fallback
        try:
            logo_img = PhotoImage(file=os.path.join("assets", "logo.png"))
            logo = Label(self.splash, image=logo_img, bg='#ffffff')
            logo.image = logo_img  # Keep reference
            logo.pack(pady=(30, 10))
        except Exception as e:
            print(f"⚠️ Logo not found: {e}")
            logo = Label(self.splash, text="🩺", font=("Arial", 48), 
                        bg='#ffffff', fg="#2e8b57")
            logo.pack(pady=(30, 10))
        
        # App title with subtle shadow effect
        title = Label(self.splash, text="HealthSync", 
                      font=("Arial", 24, "bold"), bg='#ffffff', fg="#2e8b57")
        title.pack()
        
        subtitle = Label(self.splash, text="Pet & Human Health Management", 
                        font=("Arial", 10), bg='#ffffff', fg="#555555")
        subtitle.pack(pady=(0, 20))
        
        # Modern progress bar with style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("custom.Horizontal.TProgressbar", 
                       background='#2e8b57', troughcolor='#e0e0e0')
        
        self.progress = ttk.Progressbar(self.splash, style="custom.Horizontal.TProgressbar",
                                      mode='determinate', length=300)
        self.progress.pack(pady=(0, 30))
        
        # Version info
        version = Label(self.splash, text="v1.0.0", font=("Arial", 8), 
                      bg='#ffffff', fg="#999999")
        version.pack(side='bottom', pady=5)
        
    def animate(self):
        """Run all splash screen animations"""
        self._fade_in()
        self._animate_progress()
        
    def _fade_in(self):
        alpha = self.splash.attributes('-alpha')
        if alpha < 1.0:
            alpha = min(1.0, alpha + 0.05)
            self.splash.attributes('-alpha', alpha)
            self.splash.after(30, self._fade_in)
            
    def _animate_progress(self):
        for i in range(101):
            self.splash.after(i*25, self.progress.step, 1)
        self.splash.after(2600, self._fade_out)
        
    def _fade_out(self):
        alpha = self.splash.attributes('-alpha')
        if alpha > 0:
            alpha = max(0.0, alpha - 0.05)
            self.splash.attributes('-alpha', alpha)
            self.splash.after(30, self._fade_out)
        else:
            self.splash.destroy()
            
    def run(self):
        self.splash.after(50, self.animate)
        self.splash.mainloop()

def main():
    # Initialize database
    db_manager.initialize_database()
    
    # Show splash screen
    splash = SplashScreen()
    splash.run()
    
    # Create main application window
    root = Tk()
    root.withdraw()
    
    # Configure main window
    root.title("🩺 HealthSync Pet & Human Health Management System")
    root.geometry("1000x750")
    root.configure(bg="#a3eba9")
    root.resizable(False, False)
    
    # Set window icon with better error handling
    icon_path = os.path.join("assets", "app_icon.ico")
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception as e:
            print(f"⚠️ Icon loading error: {e}")
    else:
        print(f"⚠️ Icon not found at: {icon_path}")
    
    # Fullscreen toggle with smoother transition
    def toggle_fullscreen(event=None):
        current = root.attributes("-fullscreen")
        root.attributes("-fullscreen", not current)
        if not current:  # If entering fullscreen
            root.configure(bg="#a3eba9")  # Ensure background matches
    
    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Escape>", lambda e: root.attributes("-fullscreen", False))
    
    # Initialize main app
    app = HealthSyncApp(root)
    
    # Fade in main window
    def show_main_window():
        root.deiconify()
        root.attributes('-alpha', 0.0)
        
        def fade_in(alpha=0.0):
            if alpha < 1.0:
                alpha += 0.03
                root.attributes('-alpha', alpha)
                root.after(20, fade_in, alpha)
            else:
                root.attributes('-alpha', 1.0)
        
        fade_in()
    
    # Schedule main window to appear after splash
    root.after(2700, show_main_window)
    
    root.mainloop()

if __name__ == "__main__":
    main()