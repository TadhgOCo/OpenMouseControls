import customtkinter as ctk
from PIL import Image
import mouse_hid
import threading
import time
import sys
import os

DEBUG = False

def get_full_path(relative_path):
    try:
        # PyInstaller temp folder, stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
    
def get_startup_data(properties : mouse_hid.properties, callback=None):
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

    for key, value in data.items():
        if key == "DPI Stage":
            data[key] = 1
            continue

        data[key] = value()
        time.sleep(0.01)

    return data

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
        
        img_path = get_full_path("assets/mouse.png")
        img = Image.open(img_path)

        # ctk.CTkImage
        self.img = ctk.CTkImage(
            light_image=img,
            dark_image=img,
            size=(183, 239),
        )

        self.img_btn = ctk.CTkButton(
            self,
            image=self.img,
            text="",
            fg_color="transparent",
            hover_color="#222222",
            corner_radius=15,
            command=self.start_loading,
        )

        self.img_btn.grid(row=2, column=0, pady=20)

        self.progress = ctk.CTkProgressBar(self, width=200, mode="indeterminate")
        self.progress.grid(row=3, column=0, pady=20)
        self.progress.grid_remove() # Hide loading bar

    def start_loading(self):
        self.img_btn.configure(
            state="disabled",
            image=None,
            height=239,
            width=183,
            fg_color="#333333",
            text="Connecting..."
        )

        self.progress.grid() # Show loading bar
        self.progress.start()
        
        self.spin_wait(interval=50)

    def spin_wait(self, interval=100, setup=False):
        if not setup:
            if not mouse_hid.check_perms():
                mouse_hid.install_perms()
                self.after(interval, None)
                
                if not mouse_hid.check_perms():
                    self.master.open_error_dialog("No premissions")
                    time.sleep(999999)

            self.output = [None]
            self.ConnectingThread = threading.Thread(target=mouse_hid.find_device, args=(self.output,))
            self.ConnectingThread.start()


        if not self.ConnectingThread.is_alive():
            device = self.output[0][0] if isinstance(self.output[0], list) else self.output[0]

            if device is None:
                self.master.open_error_dialog("No device found")
                time.sleep(999999)

            self.DeviceConnected.set(True)
            properties = mouse_hid.properties(device, 1, debug=DEBUG)
            def get_startup_data_task():
                data = get_startup_data(properties)
                self.after(0, lambda: self.callback(properties, data))

            threading.Thread(target=get_startup_data_task, daemon=True).start()
        else:
            self.after(interval, lambda: self.spin_wait(setup=True))


class MainPage(ctk.CTkFrame):
    def __init__(self, app: ctk.CTk, properties : mouse_hid.properties, data : dict):
        super().__init__(app, corner_radius=14)
        self.app = app
        self.properties = properties
        self.data = data
        self.grid_columnconfigure(0, weight=1)
        self.ChangedSettings = {}
        
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

        # Dropdown frame
        self.dropdown_frame = ctk.CTkFrame(self.controls, corner_radius=10)
        self.dropdown_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.dropdown_frame.grid_columnconfigure(0, weight=1)

        # Dropdowns
        PollingRateOptions = [str(opt) + " Hz" for opt in [125, 250, 500, 1000, 2000, 4000, 8000]]
        LiftOffDistOptions = [str(opt) + " mm" for opt in [0.7, 1, 2]]
        self.create_dropdowns(0, "Polling Rate", PollingRateOptions)
        self.create_dropdowns(1, "Lift-off Distance", LiftOffDistOptions)

        # Sliders frame
        self.slider_frame = ctk.CTkFrame(self.controls, corner_radius=10)
        self.slider_frame.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.slider_frame.grid_columnconfigure(0, weight=1)

        # Sliders
        self.create_slider(0, "DPI Level", 50, 42000, 50, "DPI")
        self.create_slider(2, "Debounce Time", 0, 15, 1, "ms")
        self.create_slider(3, "Sleep Timer", 15, 900, 1, "min")

        # Sync Button
        self.sync_btn = ctk.CTkButton(self.controls, text="Settings Synced", width=200, height=40, corner_radius=10, command=self.sync_btn_pressed, state="disabled")
        self.sync_btn.grid(row=7, column=0, columnspan=10, pady=(20, 0))

        self.refres_entrys(data)

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


    def create_dropdowns(self, col_idx, label, options):
        ctk.CTkLabel(self.dropdown_frame, text=label)\
            .grid(row=0, column=col_idx*2, sticky="w", padx=(5, 15), pady=5)
        
        def dropdown_update(choice):
            self.sync_btn.configure(text="Sync Settings", state="normal")
            self.ChangedSettings[label] = float(choice[:-3])
        
        combobox = ctk.CTkComboBox(self.dropdown_frame, values=options, command=dropdown_update)
        combobox.grid(row=1, column=col_idx*2, sticky="w", padx=(5, 15), pady=5)


    def create_slider(self, row_idx, label, min_v, max_v, step, unit):
        ctk.CTkLabel(self.slider_frame, text=label)\
            .grid(row=row_idx*2, column=0, sticky="w", padx=(5, 10), pady=(5,0))

        container = ctk.CTkFrame(self.slider_frame, fg_color="transparent")
        container.grid(row=row_idx*2+1, column=0, padx=(5, 5), pady=(0, 5), sticky="ew")
        container.grid_columnconfigure(0, weight=1)

        slider = ctk.CTkSlider(
            container,
            from_=min_v,
            to=max_v,
            number_of_steps=int((max_v - min_v) / step)
        )
        slider.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        entry = ctk.CTkEntry(container, width=50, justify="center")
        entry.grid(row=0, column=1)


        ctk.CTkLabel(container, text=unit, width=30, text_color="gray").grid(row=0, column=2, padx=(5, 0))

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

                if label == "Debounce Time":
                    Entryvalue = max(0, min(15, Entryvalue))
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
            self.sync_btn.configure(text="Sync Settings", state="normal")
            self.ChangedSettings[label] = value


        slider.configure(command= lambda value: slider_update(label, value))
        slider.bind("<ButtonRelease-1>", lambda event: slider_send_data(label, slider.get()))
        entry.bind("<Return>",    lambda event: entry_update(label, "Return", event))
        entry.bind("<FocusOut>",  lambda event: entry_update(label, "Focus", event))

    def update_app_state(self, label):
        self.app.IsAngleSnap = self.angle_snap.get()
        self.app.IsMotionSync = self.motion_sync.get()
        self.app.IsRippleControl = self.ripple.get()
        self.app.IsDongleLED = self.dongle_led.get()

        get_values = {
            "Angle Snap"     : self.app.IsAngleSnap,
            "Motion Sync"    : self.app.IsMotionSync,
            "Ripple Control" : self.app.IsRippleControl,
            "Dongle LED"     : self.app.IsDongleLED
        }

        self.sync_btn.configure(text="Sync Settings", state="normal")
        self.ChangedSettings[label] = get_values[label]

    def sync_btn_pressed(self):
        def ChangePageState(value):
            self.angle_snap.configure(state=value)
            self.motion_sync.configure(state=value)
            self.ripple.configure(state=value)
            self.dongle_led.configure(state=value)

            values = list(self.dropdown_frame.children.values())[1:]
            for i in range(1, len(values), 2): # Skip each label
                values[i].configure(state=value) # Each dropdown

            values = list(self.slider_frame.children.values())[1:]
            for i in range(0, len(values), 2): # Skip each label
                container = list(values[i+1].children.values())[1:]
                container[0].configure(state=value) # Slider
                container[1].configure(state=value) # Entry

        def assign_settings():
            setting_map = {
                "Angle Snap"        : self.properties.set.angle_snap,
                "Motion Sync"       : self.properties.set.motion_sync,
                "Ripple Control"    : self.properties.set.ripple_control,
                "Dongle LED"        : self.properties.set.dongle_LED,
                "DPI Level"         : lambda value: self.properties.set.dpi_stage_info(1, value),
                "Polling Rate"      : self.properties.set.polling_rate,
                "Debounce Time"     : self.properties.set.debounce_time,
                "Lift-off Distance" : self.properties.set.lift_off_dist,
                "Sleep Timer"       : self.properties.set.sleep_time
            }

            for setting_name, value in self.ChangedSettings.items():
                setting = setting_map[setting_name]
                setting(value)

            self.ChangedSettings.clear()
            return

        def refresh_screen():
            thread = threading.Thread(target=assign_settings, daemon=True)
            thread.start()
            thread.join()

            data = get_startup_data(self.properties)
            self.refres_entrys(data)

            self.sync_btn.configure(text="Settings Synced", state="disabled")
            ChangePageState("normal")

            return

        ChangePageState("disabled")
        self.sync_btn.configure(text="Syncing Settings...", state="disabled")

        thread = threading.Thread(target=refresh_screen, daemon=True)
        thread.start()


    def refres_entrys(self, data=None):
        if data is None:
            data = self.data

        if data["Angle Snap"] == True:
            self.angle_snap.select()

        if data["Motion Sync"] == True:
            self.motion_sync.select()

        if data["Ripple Control"] == True:
            self.ripple.select()

        if data["Dongle LED"] == True:
            self.dongle_led.select()

        values = list(self.dropdown_frame.children.values())[1:]
        for i in range(0, len(values), 2):
            label = values[i].cget("text")
            if label == "Lift-off Distance":
                unit = " mm"
            else:
                unit = " Hz"
            
            value = data[label]
            values[i+1].set(str(value) + unit)

        values = list(self.slider_frame.children.values())[1:]
        for i in range(0, len(values), 2):
            label = values[i].cget("text")
            value = data[label]

            container = list(values[i+1].children.values())[1:]
            container[0].set(value) # Slider
            container[1].delete(0, "end") # Entry

            if label == "Sleep Timer":
                value = round(data[label]/60)

            container[1].insert(0, str(value))

        return

    def open_firmware_info(self): # NOTE: properly Center these
        # Check if window already exists to prevent duplicates
        if hasattr(self, 'fw_window') and self.fw_window is not None and self.fw_window.winfo_exists():
            self.fw_window.lift()
            return

        self.fw_window = ctk.CTkToplevel(self)
        self.fw_window.title("Device Info")
        self.fw_window.geometry("300x220")
        self.fw_window.resizable(False, False)
        self.fw_window.attributes("-topmost", True)

        container = ctk.CTkFrame(self.fw_window, corner_radius=10)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(container, text="System Information", font=("Arial", 16, "bold"))\
            .pack(pady=(15, 20))

        # Grid for nice alignment
        info_grid = ctk.CTkFrame(container, fg_color="transparent")
        info_grid.pack(fill="x", padx=20)

        Comaptibility_grid = ctk.CTkFrame(container, fg_color="transparent")
        Comaptibility_grid.pack(fill="x", padx=20)

        DevFirmwareVersion   = "v" + self.properties.get.dev_firmware_ver()[1]
        DongleFirwareVersion = "v" + self.properties.get.dongle_firmware_ver()[1]
        
        ctk.CTkLabel(info_grid, text="Mouse FW:", text_color="gray").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        ctk.CTkLabel(info_grid, text=DevFirmwareVersion).grid(row=0, column=1, sticky="w", padx=5, pady=5,)
        
        ctk.CTkLabel(info_grid, text="Dongle FW:", text_color="gray").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        ctk.CTkLabel(info_grid, text=DongleFirwareVersion).grid(row=1, column=1, sticky="w", padx=5, pady=5)

        if DevFirmwareVersion == DongleFirwareVersion:
            Comaptibility_label = ctk.CTkLabel(Comaptibility_grid, text="Device and Dongle are fully Compatable", text_color="green", font=("Arial", 12, "bold"))
        else:
            Comaptibility_label = ctk.CTkLabel(Comaptibility_grid, text="Device and Dongle are\n NOT fully Compatable", text_color="red", font=("Arial", 12, "bold"))

        Comaptibility_label.grid(row=0, column=0, sticky="ew", padx=5, pady=10)

from os import system

if __name__ == "__main__":
    system("python -u main.py")