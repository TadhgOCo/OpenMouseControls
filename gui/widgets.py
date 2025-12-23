import mouse_hid
import customtkinter as ctk
from PIL import Image
import threading
import time

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
        self.grid_rowconfigure((0, 4), weight=1) # Center vertical content

        # 1. Welcome Text
        ctk.CTkLabel(self, text="Welcome", font=("Roboto", 24, "bold"))\
            .grid(row=1, column=0, pady=(0, 20))

        # 2. The "Image" (Button)
        # In a real app, use ctk.CTkImage here. Using a button to simulate click.
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

        # 3. Loading Bar (Hidden initially)
        self.progress = ctk.CTkProgressBar(self, width=200, mode="indeterminate")
        self.progress.grid(row=3, column=0, pady=20)
        self.progress.grid_remove() # Hide it

    def start_loading(self):
        self.img_btn.configure(state="disabled", text="Connecting...")
        self.progress.grid() # Show bar
        self.progress.start()
        
        # Wait 1 second (1000ms) then trigger callback
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
            properties = mouse_hid.properties(device, 2)
            self.get_startup_data(properties)
            return
        else:
            self.after(interval, lambda: self.spin_wait(setup=True))

    def get_startup_data(self, properties : mouse_hid.properties):
        dpi_stage = properties.get.dpi_stage()[1] - 1
        data = {
            "Angle Snap" : properties.get.angle_snap()[1],
            "Motion Sync" : properties.get.motion_sync()[1],
            "Ripple Control" : properties.get.ripple_control()[1],
            "Dongle LED" : properties.get.dongle_LED()[1],
            "DPI Level" : properties.get.dpi_stage_info()[1][dpi_stage],
            "Polling Rate" : properties.get.polling_rate()[1],
            "Debounce Time" : properties.get.debounce_time()[1],
            "Lift-off Distance" : properties.get.lift_off_dist()[1],
            "Sleep Timer" : properties.get.sleep_time()[1]
        }

        self.callback(properties, data)


class MainPage(ctk.CTkFrame):
    def __init__(self, app: ctk.CTk, properties : mouse_hid.properties, data : dict):
        super().__init__(app, corner_radius=14)
        self.app = app
        self.properties = properties
        self.data = data
        self.grid_columnconfigure(0, weight=1)
        
        # --- Top Header (Battery & Info) ---
        self.create_header()

        # --- Controls Container ---
        self.controls = ctk.CTkFrame(self, corner_radius=12, fg_color="transparent")
        self.controls.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.controls.grid_columnconfigure((0, 1), weight=1)

        # --- Title ---
        ctk.CTkLabel(
            self.controls,
            text="Mouse Settings",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=2, padx=10, pady=(0, 15), sticky="w")

        # --- Checkboxes ---
        self.create_checkboxes()

        # --- Sliders Frame ---
        self.slider_frame = ctk.CTkFrame(self.controls, corner_radius=10)
        self.slider_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.slider_frame.grid_columnconfigure(0, weight=1)

        # --- Create Sliders with Units ---
        self.create_slider(0, "DPI Level", 400, 42000, 50, "DPI")
        self.create_slider(1, "Lift-off Distance", 0.7, 2.5, 1, "mm")
        self.create_slider(2, "Debounce Time", 0, 5, 1, "ms")
        self.create_slider(3, "Polling Rate", 125, 8000, 125, "Hz")
        self.create_slider(4, "Sleep Timer", 1, 15, 1/60, "min")

    def create_header(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        header.grid_columnconfigure(0, weight=1)

        # Battery Status (Left)
        battery_frame = ctk.CTkFrame(header, fg_color="#2B2B2B", corner_radius=8)
        battery_frame.grid(row=0, column=0, sticky="w")
        
        # Battery Icon/Text
        _, Percentage, isCharging = self.properties.get.battery()
        ctk.CTkLabel(battery_frame, text=f"🔋 {Percentage}%").pack(side="left", padx=10, pady=5)

        if isCharging:
            ctk.CTkLabel(battery_frame, text="⚡ Charging", text_color="#4ade80", font=("Arial", 11)).pack(side="left", padx=(0, 10), pady=5)

        # Firmware Info Button (Right)
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
        # Label Title
        ctk.CTkLabel(self.slider_frame, text=label)\
            .grid(row=row_idx*2, column=0, sticky="w", padx=15, pady=(10, 0))

        # Container for Slider + Entry + Unit
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

        # Entry Box
        entry = ctk.CTkEntry(container, width=50, justify="center")
        entry.insert(0, str(min_v))
        entry.grid(row=0, column=1)

        value = self.data[label]
        slider.set(value)

        # Unit Label (Beside the slider/entry)
        ctk.CTkLabel(container, text=unit, width=30, text_color="gray")\
            .grid(row=0, column=2, padx=(5, 0))

        # --- Logic ---
        def slider_update(label, value):
            entry.delete(0, "end")
            if isinstance(step, int) or step.is_integer():
                entry.insert(0, int(value))
            else:
                entry.insert(0, f"{value:.1f}")

            if label == "DPI Level":
                #self.properties.set.dpi_stage_info(3, value)
                pass # NOTE: wait until the user has let go of the slider
            if label == "Lift-off Distance":
                #self.properties.set.lift_off_dist(value)
                pass
            if label == "Debounce Time":
                #self.properties.set.debounce_time(value)
                pass
            if label == "Polling Rate":
                #self.properties.set.polling_rate(value)
                pass

        def entry_update(event):
            try:
                value = float(entry.get())
                value = max(min_v, min(max_v, value))
                slider.set(value)
            except ValueError:
                pass

        slider.configure(command=lambda value: slider_update(label, value))
        entry.bind("<Return>", entry_update)
        entry.bind("<FocusOut>", entry_update)

    def update_app_state(self, data):
        self.app.IsAngleSnap = self.angle_snap.get()
        self.app.IsMotionSync = self.motion_sync.get()
        self.app.IsRippleControl = self.ripple.get()
        self.app.IsDongleLED = self.dongle_led.get()

        if data == "AngleSnap":
            self.properties.set.angle_snap(self.app.IsAngleSnap)

        if data == "MotionSync":
            self.properties.set.motion_sync(self.app.IsMotionSync)

        if data == "RippleControl":
            self.properties.set.ripple_control(self.app.IsRippleControl)

        if data == "DongleLED":
            self.properties.set.dongle_LED(self.app.IsDongleLED)

        if not self.verify_data_state():
            pass

    def verify_data_state(self):
        return True


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
        self.fw_window.attributes("-topmost", True) # Keep on top

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
        
        ctk.CTkLabel(info_grid, text="Sensor:", text_color="gray").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        ctk.CTkLabel(info_grid, text="PAW3395").grid(row=2, column=1, sticky="w", padx=5, pady=5)



from os import system
if __name__ == "__main__":
    system("python -u '/home/tocom/Documents/Python Stuff/MouseReverseEngineering/gui/app.py'")