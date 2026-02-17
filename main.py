import os
import sys
import traceback

if sys.platform == 'win32':
    # Add the hid_api.dll File
    dll_path = os.path.dirname(os.path.abspath(__file__))
    os.add_dll_directory(dll_path)

import customtkinter as ctk
from gui.widgets import MainPage, SplashScreen

NO_PREMISSION_MESSAGE = """
You do not have premission to connect to your mouse.
An attempt was made to install premissions automatically but they failded.
You can run the app with sudo privilages, or try a manual install by running the following:
`sudo bash udev/install-udev.sh $(pwd)`
This command must be run inside the project github folder at:
https://github.com/TadhgOCo/OpenMouseControls
"""

NO_DEVICE_FOUND_MESSAGE = """
The mouse was not found. For this program to work, Ensure your mouse is in dongle mode,
Ensure you have the switch on the bottom of mouse on switched to the dongle as well.
You could also try replugging your mouse and restarting your PC.
If you are on Linux, Ensure premissions are installed (see: https://github.com/TadhgOCo/OpenMouseControls)
"""

GENERAL_ERROR = """
Something has gone very wrong :-(, please report this error at:
https://github.com/TadhgOCo/OpenMouseControls/issues

Include a screenshot of this screen and a discription of what you did, along with our OS and Mouse model.
Also run this app in the terminal and paste the error into your bug report.

Error Captured:

"""

DEVICE_NOT_SUPPORTED = """
The device you have selected is not supported, If you belive it should be,
Ensure you have the latest version of this program and unplug all other Attackshark Products and try again.
An updated list of compatable products can be found at:
https://github.com/TadhgOCo/OpenMouseControls/blob/main/README.md
"""

DEVICE_UNTESTED_MESSAGE = """
This Device is unstested with this software, but meets all of the requirements to function properly.
i.e There is no reason this program shouldn't work as intended although not all mouse features will be available, eg. Lighting Control

If you have tested this software on a product that triggers this warning, create an issue at:
https://github.com/TadhgOCo/OpenMouseControls/issues

Click Exit to Close the program or Continue to resume.
"""

DEVICE_PARTAILLY_SUPPORTED_MESSAGE = """
This Device may be partailly supported and is unstest with this software, but meets most of the requirements to function properly.
i.e There is no reason this program shouldn't work as intended although not all software features will be available, eg. Profile Switching
Unsupported features will be greyed out.

Click Exit to Close the program or Continue to resume.
"""

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.report_callback_exception = self.global_error_handler

        # Window Setup
        self.geometry("400x600")
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

    def show_main_page(self, properties, data, is_Supported, device_name):
        if is_Supported != "Verified":
            if is_Supported == "Partial":
                self.open_warning_dialog("Device Partailly Supported")
            if is_Supported == "Untested":
                self.open_warning_dialog("Device Untested")
            if is_Supported == "Not":
                self.open_error_dialog("Device NOT supported")

        # Destroy splash and build main page
        self.splash.destroy()
        self.main_page = MainPage(self, properties, data, device_name, self.open_warning_dialog)
        self.main_page.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def global_error_handler(self, exc, val, tb):
        error_msg = "".join(traceback.format_exception(exc, val, tb))
        print(error_msg) # Print to console for debugging
        self.open_error_dialog("CRITICAL ERROR", str(val))

    def open_warning_dialog(self, warning_title, warning_msg="", fatal=False):
        # Prevent duplicate windows
        if hasattr(self, 'fw_window') and self.fw_window.winfo_exists():
            self.fw_window.lift()
            return

        def kill_program():
            try:
                self.fw_window.destroy()
                self.quit()
            finally:
                exit(1)

        def continue_program():
            self.fw_window.destroy()

        self.fw_window = ctk.CTkToplevel(self)
        self.fw_window.title("OpenMouseControl - WARNING")
        self.fw_window.geometry("530x400")
        self.fw_window.resizable(False, False)
        self.fw_window.attributes("-topmost", True)

        self.fw_window.protocol("WM_DELETE_WINDOW", continue_program)

        container = ctk.CTkFrame(self.fw_window, corner_radius=10)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        ctk.CTkLabel(
            container,
            text=f"⚠ Warning: {warning_title}",
            font=("Arial", 18, "bold"),
            text_color="#F5A623"  # orange/yellow
        ).pack(pady=(20, 10))

        messages = {
            "Device Untested": DEVICE_UNTESTED_MESSAGE,
            "Device Partailly Supported": DEVICE_PARTAILLY_SUPPORTED_MESSAGE,
        }

        display_text = messages.get(warning_title, GENERAL_ERROR + warning_msg)

        # Message body
        ctk.CTkLabel(
            container,
            text=display_text,
            font=("Arial", 14),
            wraplength=450,
            justify="left"
        ).pack(pady=10, padx=20)

        # Buttons
        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(side="bottom", pady=20)

        ctk.CTkButton(
            button_frame,
            text="Continue",
            command=continue_program,
            fg_color="#2E8B57",     # green
            hover_color="#256F46"
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="Exit Application",
            command=kill_program,
            fg_color="#CC3333",
            hover_color="#992222"
        ).pack(side="left", padx=10)

        self.fw_window.grab_set()
        self.wait_window(self.fw_window)


    def open_error_dialog(self, error_title, error_msg="", fatal=True):
        # Check if window already exists to prevent duplicates
        if hasattr(self, 'fw_window') and self.fw_window.winfo_exists():
            self.fw_window.lift()
            return
        
        def kill_program():
            self.fw_window.destroy()

            if fatal:
                try:
                    self.quit()
                finally:
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
            "No premissions": NO_PREMISSION_MESSAGE,
            "No device found": NO_DEVICE_FOUND_MESSAGE,
            "Device NOT supported" : DEVICE_NOT_SUPPORTED
        }
        
        # dict.get(key, default)
        display_text = messages.get(error_title, GENERAL_ERROR+error_msg)

        ctk.CTkLabel(container, text=display_text, font=("Arial", 14), wraplength=450, justify="left")\
            .pack(pady=10, padx=20)

        ctk.CTkButton(
            container, 
            text="Exit Application", 
            command=kill_program,
            fg_color="#CC3333", 
            hover_color="#992222"
        ).pack(side="bottom", pady=20)


        self.fw_window.grab_set()
        self.wait_window(self.fw_window)


if __name__ == "__main__":
    app = App()
    app.mainloop()