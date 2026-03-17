import customtkinter as ctk
from PIL import Image
import mouse_hid
import threading
import time
import sys
import os

DEBUG = False

ModelDataList = {
    # "MODEL_NAME" : "Max_DPI,Max_Polling_Rate,Protocal_Version,Product_ID"
    "X3": "26000,1000,v3,?",
    "X3 PRO": "26000,8000,v3,?",
    "X3 MAX": "42000,1000,v3,?",
    "X8 SE": "25000,1000,v3,?",
    "X8 PLUS": "40000,1000,v3,?",
    "X8 PRO": "40000,8000,v3,?",
    "X8 ULTRA": "42000,8000,v3,?",
    "X8 ULTIMATE": "42000,8000,v3,?",
    "X11": "22000,1000,v3,?",
    "X11 SE": "22000,1000,v3,?",
    "R11 ULTRA": "42000,8000,v?,?",
    "R5 ULTRA": "42000,8000,v3,?",
    "G3": "22000,1000,v3,?",
    "G3 PRO": "25000,1000,v3,?",

    "X6": "26000,1000,v?,?",
    "R1": "18000,1000,v?,?",
    "R3": "26000,8000,v3,?",
    "X1": "40000,1000,v?,?",
    "R2": "42000,8000,v?,?",
    "X5": "4000,250,v?,?",
    "X2": "4000,250,v?,?",
    "V6": "25000,1000,v?,?",
    "V3": "25000,1000,v?,?",
    "V5": "42000,8000,v?,?",
    "R6": "42000,8000,v2,61476",
}

MODEL_DATA = {}
for model in ModelDataList.keys():
    data = ModelDataList[model].split(",")

    if data[3] == "?":
        pid = "?"
    else:
        pid = int(data[3])

    MODEL_DATA[model] = {
        "Max_DPI" : int(data[0]),
        "Max_Polling_Rate" : int(data[1]),
        "Protocal_Version" : data[2],
        "Product_ID" : pid,
    }
    
Verified_Supported_PIDs = []
Untested_PIDs = []
Partially_Supported_PIDs = []
Not_Supported_PIDs = []

for model in MODEL_DATA.keys():
    if MODEL_DATA[model]["Protocal_Version"] == "v2" and MODEL_DATA[model]["Product_ID"] != "?":
        Verified_Supported_PIDs.append(MODEL_DATA[model]["Product_ID"])

    elif MODEL_DATA[model]["Protocal_Version"] == "v2":
        Untested_PIDs.append(MODEL_DATA[model]["Product_ID"])

    elif MODEL_DATA[model]["Protocal_Version"] == "v1":
        Partially_Supported_PIDs.append(MODEL_DATA[model]["Product_ID"])

    elif MODEL_DATA[model]["Protocal_Version"] == "v3":
        Not_Supported_PIDs.append(MODEL_DATA[model]["Product_ID"])

def get_full_path(relative_path):
    try:
        # PyInstaller temp folder, stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
    
def get_startup_data(properties : mouse_hid.properties):

    Success, ProductID = properties.get.PID()

    if Success == False:
        is_Supported = "Not"

    if ProductID in Verified_Supported_PIDs:
        is_Supported = "Verified"
        Protocal_ver = "v2"

    elif ProductID in Untested_PIDs:
        is_Supported = "Untested"
        Protocal_ver = "v2"

    elif ProductID in Partially_Supported_PIDs:
        is_Supported = "Partial"
        Protocal_ver = "v1"
        
    elif ProductID in Not_Supported_PIDs:
        is_Supported = "Not"
        Protocal_ver = "v3"

    if is_Supported == "Not":
        return is_Supported, Protocal_ver, []

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
        "PID"               : lambda: properties.get.PID()[1],

        "DPI Stage"         : 1
    }

    for key, value in data.items():
        if key == "DPI Stage":
            data[key] = 1
            continue

        data[key] = value()
        time.sleep(0.01)

    return is_Supported, Protocal_ver, data

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
            size=(310, 310),
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
            if mouse_hid.check_device():
                if not mouse_hid.check_perms():
                    mouse_hid.install_perms()
                    self.after(interval, None)
                    
                    if not mouse_hid.check_perms():
                        self.master.open_error_dialog("No Premissions", fatal=True)
                        self.master.destroy()
            else:
                self.master.open_error_dialog("No Device", fatal=True)

            self.output = [None]
            self.ConnectingThread = threading.Thread(target=mouse_hid.find_device, args=(self.output,))
            self.ConnectingThread.start()


        if not self.ConnectingThread.is_alive():
            device, product_name = self.output[0][0] if isinstance(self.output[0], list) else self.output[0]

            if device is None:
                self.master.open_error_dialog("No device found", fatal=True)
                self.master.destroy()

            self.DeviceConnected.set(True)
            orginal_properties = mouse_hid.properties(device, ProfileID=1, debug=DEBUG)
            def get_startup_data_task():
                properties = orginal_properties
                is_Supported, Protocal_ver, data = get_startup_data(properties)

                if Protocal_ver == "v1":
                    properties = mouse_hid.properties(device, ProfileID=-1, debug=DEBUG)

                # R6 Mouse 2.4G
                if product_name[1] in mouse_hid.SUFFIX_LIST:
                    device_name = product_name[0] + product_name[1]
                else:
                    device_name = product_name[0]

                for model in MODEL_DATA.keys():
                    if device_name == model:
                        break

                self.after(0, lambda: self.callback(properties, data, is_Supported, device_name))

            threading.Thread(target=get_startup_data_task, daemon=True).start()
        else:
            self.after(interval, lambda: self.spin_wait(setup=True))


class MainPage(ctk.CTkFrame):
    def __init__(self, app: ctk.CTk, properties : mouse_hid.properties, data : dict, device_name : str, warning_dialog : callable):
        super().__init__(app, corner_radius=14)
        self.app = app
        self.properties = properties
        self.data = data
        self.grid_columnconfigure(0, weight=1)
        self.ChangedSettings = {}
        self.slider_widgets = {}
        self.is_refreshing = False
        self.CurrentProfile = int(self.properties.get.profile_id()[1])
        self.warning_screen = warning_dialog

        self.protocal_ver = MODEL_DATA[device_name]["Protocal_Version"]
        self.DPI_Max = MODEL_DATA[device_name]["Max_DPI"]
        self.Polling_Rate_Max = MODEL_DATA[device_name]["Max_Polling_Rate"]
        
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


        if self.protocal_ver == "v2":
            # Profile Switcher
            ProfileFrame = ctk.CTkFrame(self.controls, corner_radius=10)
            ProfileFrame.grid(row=0, column=2, padx=10, pady=(0, 15), sticky="e")
            
            combobox = ctk.CTkComboBox(ProfileFrame, values=[f"Profile: {i+1}" for i in range(3)], command=self.update_profiles)
            combobox.grid(row=0, column=2, columnspan=2, sticky="w", padx=(5, 10), pady=5)
            combobox.set(f"Profile: {self.CurrentProfile}")


        self.create_checkboxes()

        # Dropdown frame
        self.dropdown_frame = ctk.CTkFrame(self.controls, corner_radius=10)
        self.dropdown_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.dropdown_frame.grid_columnconfigure(0, weight=1)

        # Dropdowns
        Polling_rate_list = [125, 250, 500, 1000, 2000, 4000, 8000]
        Max_idx = Polling_rate_list.index(self.Polling_Rate_Max)
        Polling_rate_list = Polling_rate_list[:Max_idx+1]

        PollingRateOptions = [str(opt) + " Hz" for opt in Polling_rate_list]
        LiftOffDistOptions = [str(opt) + " mm" for opt in [0.7, 1, 2]]
        self.create_dropdowns(0, "Polling Rate", PollingRateOptions)
        self.create_dropdowns(1, "Lift-off Distance", LiftOffDistOptions)

        # Sliders frame
        self.slider_frame = ctk.CTkFrame(self.controls, corner_radius=10)
        self.slider_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        self.slider_frame.grid_columnconfigure(0, weight=1)

        # Sliders
        self.create_slider(0, "DPI Level", 50, self.DPI_Max, 50, "DPI")
        self.create_slider(2, "Debounce Time", 0, 15, 1, "ms")
        self.create_slider(3, "Sleep Timer", 15, 900, 1, "min")

        # Sync Button
        self.sync_btn = ctk.CTkButton(self.controls, text="Settings Synced", width=200, height=40, corner_radius=10, command=self.sync_btn_pressed, state="disabled")
        self.sync_btn.grid(row=7, column=0, columnspan=3, pady=(20, 0))

        self.refresh_entrys(data)

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

        self.angle_snap.grid(row=1, column=0, columnspan=3, sticky="w", pady=6, padx=15)
        self.motion_sync.grid(row=1, column=2, columnspan=3, sticky="w", pady=6, padx=15)
        self.ripple.grid(row=2, column=0, columnspan=3, sticky="w", pady=6, padx=15)
        self.dongle_led.grid(row=2, column=2, columnspan=3, sticky="w", pady=6, padx=15)


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

        self.slider_widgets[label] = {
                    "slider": slider,
                    "entry": entry
                }


        ctk.CTkLabel(container, text=unit, width=30, text_color="gray").grid(row=0, column=2, padx=(5, 0))

        def slider_update(label, value):
            if not self.is_refreshing:
                entry.delete(0, "end")
                EntryValue = round(value/60) if label == "Sleep Timer" else value
                if isinstance(step, int) or step.is_integer():
                    entry.insert(0, int(EntryValue))
                else:
                    entry.insert(0, f"{EntryValue:.1f}")

        def entry_update(label, EvType, event):
            if not self.is_refreshing:

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

                    if EvType == "Return":
                        slider_send_data(label, slider.get())

                except ValueError as e:
                    print(f"Value Error:\n{e}")

        def slider_send_data(label, value):
            if not self.is_refreshing:
                value = int(value)
                self.sync_btn.configure(text="Sync Settings", state="normal")
                self.ChangedSettings[label] = value


        slider.configure(command= lambda value: slider_update(label, value))
        slider.bind("<ButtonRelease-1>", lambda event: slider_send_data(label, slider.get()))
        entry.bind("<Return>",    lambda event: entry_update(label, "Return", event))
        entry.bind("<FocusOut>",  lambda event: entry_update(label, "Focus", event))

    def update_app_state(self, label):
        if self.is_refreshing:
            print("Refreshing (ln: 337)")
            return

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

    def sync_btn_pressed(self, AssignSettings=True):
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
                time.sleep(0.03)

            self.ChangedSettings.clear()
            return
        
        def finish_ui_update(data):
            self.data = data
            ChangePageState("normal")

            self.refresh_entrys(data)

            self.sync_btn.configure(text="Settings Synced", state="disabled")

        def refresh_screen(AssignSettings=True):
            if AssignSettings:
                assign_settings()

            _, _, data = get_startup_data(self.properties)
            self.after(0, lambda: finish_ui_update(data))

        ChangePageState("disabled")
        self.sync_btn.configure(text="Syncing Settings...", state="disabled")

        thread = threading.Thread(target=lambda: refresh_screen(AssignSettings), daemon=True)
        thread.start()

    def update_profiles(self, choice):
        profile = int(choice.split(":")[-1].strip())

        self.CurrentProfile = profile
        self.properties.set_profile(profile)

        self.ChangedSettings = self.data.copy()
        self.ChangedSettings.clear()
        self.sync_btn_pressed(AssignSettings=False)


    def refresh_entrys(self, data=None):
        self.is_refreshing = True

        if data is None:
            data = self.data

        if data["Angle Snap"] == True:
            self.angle_snap.select()
        else:
            self.angle_snap.deselect()

        if data["Motion Sync"] == True:
            self.motion_sync.select()
        else:
            self.motion_sync.deselect()

        if data["Ripple Control"] == True:
            self.ripple.select()
        else:
            self.ripple.deselect()

        if data["Dongle LED"] == True:
            self.dongle_led.select()
        else:
            self.dongle_led.deselect()

        values = list(self.dropdown_frame.children.values())[1:]
        for i in range(0, len(values), 2):
            label = values[i].cget("text")
            if label == "Lift-off Distance":
                unit = " mm"
            else:
                unit = " Hz"
            
            num = data[label]
            values[i+1].set(str(num) + unit)

        for label, widgets in self.slider_widgets.items():
            if label in data:
                num = data[label]
                slider = widgets["slider"]
                entry = widgets["entry"]

                slider.set(num) 

                if label == "Sleep Timer":
                    display_value = str(round(num / 60))
                else:
                    display_value = str(num)

                entry.delete(0, "end")
                entry.insert(0, display_value)

        self.is_refreshing = False

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