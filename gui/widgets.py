import mouse_hid
import customtkinter as ctk
from PIL import Image
import threading
import time
from tkinter import Event

def cheack_connected(ConnectingThread : threading.Thread):
    if ConnectingThread.is_alive():
        return False
    else:
        return True
    

class SplashScreen(ctk.CTkFrame):
    def __init__(self, master, callback):
        self.master = master
        super().__init__(master)
        self.DeviceConnected = ctk.BooleanVar(value=False)
        self.callback = callback
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 4), weight=1)

        ctk.CTkLabel(self, text="Welcome", font=("Roboto", 24, "bold"))\
            .grid(row=1, column=0, pady=(0, 20))

        # ctk.CTkImage
        self.img_btn = ctk.CTkButton(
            self, 
            text="[ Click Mouse Image ]", 
            height=150, 
            width=200,
            fg_color="#333333",
            hover_color="#444444",
            corner_radius=15,
            command=self.start_loading
        )
        self.img_btn.grid(row=2, column=0, pady=20)

        self.progress = ctk.CTkProgressBar(self, width=200, mode="indeterminate")
        self.progress.grid(row=3, column=0, pady=20)
        self.progress.grid_remove() # Hide loading bar

    def start_loading(self):
        self.img_btn.configure(state="disabled", text="Connecting...")
        self.progress.grid() # Show loading bar
        self.progress.start()
        
        self.spin_wait(interval=1000) 

    def spin_wait(self, interval=100, setup=False):
        if not setup:
            if not mouse_hid.check_perms():
                mouse_hid.install_perms()
                self.after(interval, None)
                
            if not mouse_hid.check_perms():
                print("No premissions")
                exit(1) # NOTE: Make Better

            self.output = [[None]] # NOTE: Figure out why i have to double wrap this
            self.ConnectingThread = threading.Thread(target=mouse_hid.find_device, args=self.output)
            self.ConnectingThread.start()


        if cheack_connected(self.ConnectingThread):
            while True: # NOTE: Imrpve this, look at line 64 (spin wait)
                if type(self.output[0]) == list:
                    self.output = self.output[0]
                else:
                    device = self.output[0]
                    break
                    

            if device == None:
                print("No device found")
                exit(1) # NOTE: Make Better

            self.DeviceConnected.set(True)
            properties = mouse_hid.properties(device, 1)
            self.get_startup_data(properties)
            return
        else:
            self.after(interval, lambda: self.spin_wait(setup=True))

    def get_startup_data(self, properties : mouse_hid.properties):
        dpi_stage = properties.get.dpi_stage()[1]
        if dpi_stage != 1:
            properties.set.dpi_stage(1)
            time.sleep(0.03)

        data = {
            "Angle Snap"        : lambda: properties.get.angle_snap()[1],
            "Motion Sync"       : lambda: properties.get.motion_sync()[1],
            "Ripple Control"    : lambda: properties.get.ripple_control()[1],
            "Dongle LED"        : lambda: properties.get.dongle_LED()[1],
            "DPI Level"         : lambda: properties.get.dpi_stage_info(6)[1][0],
            "Polling Rate"      : lambda: properties.get.polling_rate()[1],
            "Debounce Time"     : lambda: properties.get.debounce_time()[1],
            "Lift-off Distance" : lambda: properties.get.lift_off_dist()[1],
            "Sleep Timer"       : lambda: properties.get.sleep_time()[1],

            "DPI Stage"         : 1
        }

        i = 0
        for key, value in data.items():
            if i == 9:
                break

            data[key] = value()
            time.sleep(0.01)
            i += 1

        self.callback(properties, data)


class MainPage(ctk.CTkFrame):
    def __init__(self, app: ctk.CTk, properties : mouse_hid.properties, data : dict):
        super().__init__(app, corner_radius=14)
        self.app = app
        self.properties = properties
        self.data = data
        self.grid_columnconfigure(0, weight=1)
        
        # Battery + Firmware Info
        self.create_header()

        # Controls
        self.controls = ctk.CTkFrame(self, corner_radius=12, fg_color="transparent")
        self.controls.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.controls.grid_columnconfigure((0, 1), weight=1)

        # Window title
        ctk.CTkLabel(
            self.controls,
            text="Mouse Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=(0, 15), sticky="w")

        self.create_checkboxes()

        # Sliders frame
        self.slider_frame = ctk.CTkFrame(self.controls, corner_radius=10)
        self.slider_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.slider_frame.grid_columnconfigure(0, weight=1)

        # Sliders
        self.create_slider(0, "DPI Level", 50, 42000, 50, "DPI")
        self.create_slider(1, "Lift-off Distance", 0.7, 2.5, 0.1, "mm") # NOTE: Change to a combobox
        self.create_slider(2, "Debounce Time", 0, 15, 1, "ms")
        self.create_slider(3, "Polling Rate", 125, 8000, 125, "Hz") # NOTE: Change to a combobox
        self.create_slider(4, "Sleep Timer", 1, 900, 1, "min")

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        header.grid_columnconfigure(0, weight=1)

        battery_frame = ctk.CTkFrame(header, fg_color="#2B2B2B", corner_radius=8)
        battery_frame.grid(row=0, column=0, sticky="w")
        
        _, Percentage, isCharging = self.properties.get.battery()
        ctk.CTkLabel(battery_frame, text=f"🔋 {Percentage}%").pack(side="left", padx=10, pady=5)

        # If the battery is charging 
        if isCharging:
            ctk.CTkLabel(battery_frame, text="⚡ Charging", text_color="#4ade80", font=("Arial", 11)).pack(side="left", padx=(0, 10), pady=5)

        # Firmware Button
        self.info_btn = ctk.CTkButton(
            header, 
            text="?", 
            width=30, 
            height=30, 
            corner_radius=15,
            font=("Arial", 14, "bold"),
            command=self.open_firmware_info
        )
        self.info_btn.grid(row=0, column=1, sticky="e")

    def create_checkboxes(self):
        # Local references for callbacks
        self.angle_snap = ctk.CTkCheckBox(self.controls, text="Angle Snap",   command= lambda: self.update_app_state("Angle Snap"))
        self.motion_sync = ctk.CTkCheckBox(self.controls, text="Motion Sync", command= lambda: self.update_app_state("Motion Sync"))
        self.ripple = ctk.CTkCheckBox(self.controls, text="Ripple Control",   command= lambda: self.update_app_state("Ripple Control"))
        self.dongle_led = ctk.CTkCheckBox(self.controls, text="Dongle LED",   command= lambda: self.update_app_state("Dongle LED"))

        self.angle_snap.grid(row=1, column=0, sticky="w", pady=6, padx=15)
        self.motion_sync.grid(row=1, column=1, sticky="w", pady=6, padx=15)
        self.ripple.grid(row=2, column=0, sticky="w", pady=6, padx=15)
        self.dongle_led.grid(row=2, column=1, sticky="w", pady=6, padx=15)
        
        if self.data["Angle Snap"] == True:
            self.angle_snap.select()

        if self.data["Motion Sync"] == True:
            self.motion_sync.select()

        if self.data["Ripple Control"] == True:
            self.ripple.select()

        if self.data["Dongle LED"] == True:
            self.dongle_led.select()


    def create_slider(self, row_idx, label, min_v, max_v, step, unit):
        ctk.CTkLabel(self.slider_frame, text=label)\
            .grid(row=row_idx*2, column=0, sticky="w", padx=15, pady=(10, 0))

        container = ctk.CTkFrame(self.slider_frame, fg_color="transparent")
        container.grid(row=row_idx*2+1, column=0, padx=10, pady=(0, 5), sticky="ew")
        container.grid_columnconfigure(0, weight=1)

        var = ctk.DoubleVar(value=min_v)

        slider = ctk.CTkSlider(
            container,
            from_=min_v,
            to=max_v,
            number_of_steps=int((max_v - min_v) / step),
            variable=var
        )
        slider.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        value = self.data[label]
        slider.set(value)

        entry = ctk.CTkEntry(container, width=50, justify="center")
        value = round(value/60) if label == "Sleep Timer" else value
        entry.insert(0, str(value))
        entry.grid(row=0, column=1)


        ctk.CTkLabel(container, text=unit, width=30, text_color="gray")\
            .grid(row=0, column=2, padx=(5, 0))

        def slider_update(label, value):
            entry.delete(0, "end")
            EntryValue = round(value/60) if label == "Sleep Timer" else value
            if isinstance(step, int) or step.is_integer():
                entry.insert(0, int(EntryValue))
            else:
                entry.insert(0, f"{EntryValue:.1f}")

        def entry_update(label, EvType, event):
            if EvType == "Return":
                slider_send_data(label, slider.get())

            try:
                Entryvalue = float(entry.get())
                value = Entryvalue

                if label == "DPI Level":
                    Entryvalue = max(50, min(42000, Entryvalue))
                    Entryvalue = round(Entryvalue)
                    value = round(Entryvalue)

                if label == "Lift-off Distance":
                    Entryvalue = max(0.7, min(2, Entryvalue))
                    Entryvalue = round(Entryvalue, 1)
                    value = round(Entryvalue)

                if label == "Debounce Time":
                    Entryvalue = max(0, min(15, Entryvalue))
                    Entryvalue = round(Entryvalue)
                    value = round(Entryvalue)

                if label == "Polling Rate":
                    Entryvalue = max(125, min(8000, Entryvalue))
                    Entryvalue = round(Entryvalue)
                    value = round(Entryvalue)

                if label == "Sleep Timer":
                    Entryvalue = max(1, min(15, Entryvalue))
                    Entryvalue = round(Entryvalue)
                    value = round(Entryvalue*60)

                entry.delete(0, "end")
                entry.insert(0, f"{Entryvalue}")

                slider.set(value)
            except ValueError:
                pass

        def slider_send_data(label, value):
            value = int(value)

            if label == "DPI Level":
                self.properties.set.dpi_stage_info(1, value)

            if label == "Lift-off Distance":
                #self.properties.set.lift_off_dist(value) # NOTE: Need to observe source code
                pass

            if label == "Debounce Time":
                self.properties.set.debounce_time(value)

            if label == "Polling Rate":
                self.properties.set.polling_rate(value)

            if label == "Sleep Timer":
                self.properties.set.sleep_time(value)


        slider.configure(command= lambda value: slider_update(label, value))
        slider.bind("<ButtonRelease-1>", lambda event: slider_send_data(label, slider.get()))
        entry.bind("<Return>",    lambda event: entry_update(label, "Return", event))
        entry.bind("<FocusOut>",  lambda event: entry_update(label, "Focus", event))

    def update_app_state(self, data):
        self.app.IsAngleSnap = self.angle_snap.get()
        self.app.IsMotionSync = self.motion_sync.get()
        self.app.IsRippleControl = self.ripple.get()
        self.app.IsDongleLED = self.dongle_led.get()

        if data == "Angle Snap":
            self.properties.set.angle_snap(self.app.IsAngleSnap)

        if data == "Motion Sync":
            self.properties.set.motion_sync(self.app.IsMotionSync)

        if data == "Ripple Control":
            self.properties.set.ripple_control(self.app.IsRippleControl)

        if data == "Dongle LED":
            self.properties.set.dongle_LED(self.app.IsDongleLED)


    def open_firmware_info(self):
        # Check if window already exists to prevent duplicates
        if hasattr(self, 'fw_window') and self.fw_window is not None and self.fw_window.winfo_exists():
            self.fw_window.lift()
            return

        self.fw_window = ctk.CTkToplevel(self)
        self.fw_window.title("Device Info")
        self.fw_window.geometry("300x200")
        self.fw_window.minsize(300,200)
        self.fw_window.maxsize(300,200)
        self.fw_window.attributes("-topmost", True)

        container = ctk.CTkFrame(self.fw_window, corner_radius=10)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(container, text="System Information", font=("Arial", 16, "bold"))\
            .pack(pady=(15, 20))

        # Grid for nice alignment
        info_grid = ctk.CTkFrame(container, fg_color="transparent")
        info_grid.pack(fill="x", padx=20)
        
        ctk.CTkLabel(info_grid, text="Mouse FW:", text_color="gray").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ctk.CTkLabel(info_grid, text="v1.0.4").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        ctk.CTkLabel(info_grid, text="Dongle FW:", text_color="gray").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ctk.CTkLabel(info_grid, text="v1.2.0").grid(row=1, column=1, sticky="w", padx=5, pady=5)

from os import system

if __name__ == "__main__":
    system("python -u '/home/tocom/Documents/Python Stuff/MouseReverseEngineering/gui/app.py'")