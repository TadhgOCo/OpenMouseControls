import os
import sys
import traceback

if sys.platform == 'win32':
    # Add the hid_api.dll File
    dll_path = os.path.dirname(os.path.abspath(__file__))
    os.add_dll_directory(dll_path)

import customtkinter as ctk
from gui.widgets import MainPage, SplashScreen

NOPREMISSIONMESSAGE = """
You do not have premission to connect to your mouse.
An attempt was made to install premissions automatically but they failded.
You can run the app with sudo privilages, or try a manual install by running the following:
`sudo bash udev/install-udev.sh $(pwd)`
This command must be run inside the project github folder at:
https://github.com/TadhgOCo/OpenMouseControls
"""

NODEVICEFOUNDMESSAGE = """
The mouse was not found. You must be in dongle mode, for this program to work
Ensure you have the switch on the bottom of mouse on switched to the dongle as well.
You could also try replugging your mouse and restarting your PC.
"""

GENERALERROR = """
Something has gone very wrong :-(, please report this error at:
https://github.com/TadhgOCo/OpenMouseControls/issues
Include a screenshot of this screen and a discription of what you did, along with our OS and Mouse.
Also run this app in the terminal and paste the error into your bug report.
Error Captured:

"""

# Set appearance before initializing the app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.report_callback_exception = self.global_error_handler

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

        self.show_splash_screen()

    def show_splash_screen(self):
        self.splash = SplashScreen(self, self.show_main_page)
        self.splash.grid(row=0, column=0, sticky="nsew")

    def show_main_page(self, properties, data):
        # Destroy splash and build main page
        self.splash.destroy()
        self.main_page = MainPage(self, properties, data)
        self.main_page.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def global_error_handler(self, exc, val, tb):
        error_msg = "".join(traceback.format_exception(exc, val, tb))
        print(error_msg) # Still print to console for debugging
        self.open_error_dialog("CRITICAL ERROR", str(val))

    def open_error_dialog(self, error_title, error_msg=""):
        # Check if window already exists to prevent duplicates
        if hasattr(self, 'fw_window') and self.fw_window.winfo_exists():
            self.fw_window.lift()
            return
        
        def kill_program():
            root = self.winfo_toplevel()
            root.destroy()
            exit(1)

        self.fw_window = ctk.CTkToplevel(self)
        self.fw_window.title("OpenMouseControl - ERROR")
        self.fw_window.geometry("530x400")
        self.fw_window.resizable(False, False)
        self.fw_window.attributes("-topmost", True)

        # When the user presses the X button
        self.fw_window.protocol("WM_DELETE_WINDOW", kill_program)

        container = ctk.CTkFrame(self.fw_window, corner_radius=10)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(container, text=f"⚠ Error: {error_title}", font=("Arial", 18, "bold"), text_color="#FF5555")\
            .pack(pady=(20, 10))
        
        messages = {
            "No premissions": NOPREMISSIONMESSAGE,
            "No device found": NODEVICEFOUNDMESSAGE,
        }
        
        display_text = messages.get(error_title, GENERALERROR+error_msg)

        ctk.CTkLabel(container, text=display_text, font=("Arial", 14), wraplength=450, justify="left").pack(pady=10, padx=20)

        ctk.CTkButton(
            container, 
            text="Exit Application", 
            command=kill_program,
            fg_color="#CC3333", 
            hover_color="#992222"
        ).pack(side="bottom", pady=20)


if __name__ == "__main__":
    app = App()
    app.mainloop()