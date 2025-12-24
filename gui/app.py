#import mouse_hid
import customtkinter as ctk
import time
from widgets import MainPage, SplashScreen

# Set appearance before initializing the app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.geometry("400x600") # Increased height to fit new settings
        self.minsize(400, 600)
        self.maxsize(800, 900)
        self.title("Mouse Control Panel")

        # Global State Variables
        self.IsAngleSnap = False
        self.IsDongleLED = False
        self.IsMotionSync = False
        self.IsRippleControl = False
        
        # Grid Configuration for the main window container
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Start with the Splash Screen
        self.show_splash_screen()

    def show_splash_screen(self):
        self.splash = SplashScreen(self, self.show_main_page)
        self.splash.grid(row=0, column=0, sticky="nsew")

    def show_main_page(self, properties, data):
        # Destroy splash and build main page
        self.splash.destroy()
        self.main_page = MainPage(self, properties, data)
        self.main_page.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()


#dev = mouse_hid.find_device()
#properites = mouse_hid.properties(dev, 2)

#if not dev:
#    print("No compatible device found.")
#    exit()

#try:
#    out = properites.get.battery()
#    print(out)
#finally:
#    dev.close()