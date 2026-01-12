import mouse_hid.protocal_cmd as protocal_cmd
import time
import hid
import sys

DEBUG = False

def send_command(device : hid.Device, packet, NoGetFeature=False):
    device.send_feature_report(packet)
    if NoGetFeature == False:
        time.sleep(0.03)
        response = device.get_feature_report(0x02, 65)

        if response != 0xA1:
            for _ in range(5):
                if response[0] > 0xA1:
                    device.send_feature_report(packet)
                    time.sleep(0.03)
                    response = device.get_feature_report(0x02, 65)
                    time.sleep(0.1)
                else:
                    break

            for _ in range(3):
                if response[1] < 0xA1:
                    device.send_feature_report(packet)
                    time.sleep(0.03)
                    response = device.get_feature_report(0x02, 65)
                    time.sleep(0.1)
                else:
                    break

        if response[0] == 0xA1 or response[1] == 0xA1:
            Success = True
            if DEBUG == True:
                print("Success: Device acknowledged command (0xA1).")

        else:
            Success = False
            if DEBUG == True:
                print(f"Warning: Device did not return success code. Raw: {response[:5]}")

    else:
        Success, response = (True, [])

    if sys.platform == "win32":
        # When running on windows remove the initial byte of overhead
        response = response[1:]

    if Success == False:
        print(f"ERROR: Device did not return success code. Raw: {response[:5]}")

    return Success, response


class properties:
    def __init__(self, dev : hid.Device, profileID : int = -1, debug=False):
        global DEBUG

        DEBUG = debug

        if profileID != -1:
            profileID = min(max(profileID, 1), 3)

        self.get = GET(dev, profileID)
        self.set = SET(dev, profileID)

class GET:
    def __init__(self, dev : hid.Device, profileID : int = -1):
        self.profileID = profileID
        self.device = dev

    def angle_snap(self):
        Success, response = send_command(self.device, protocal_cmd.get_angle_snap(self.profileID))

        if self.profileID == -1:
            isEnabled = response[6]
        else:
            isEnabled = response[7]

        return Success, isEnabled
    
    def debounce_time(self):
        Success, response = send_command(self.device, protocal_cmd.get_debounce(self.profileID))

        DebounceTime = response[7]

        return Success, DebounceTime
    
    def dongle_LED(self):
        Success, response = send_command(self.device, protocal_cmd.get_dongle_LED(self.profileID))

        isEnabled = response[7]
        return Success, isEnabled
    
    def battery(self):
        Success, response = send_command(self.device, protocal_cmd.get_battery())

        isChrarging = response[6]
        percentage = response[7]

        return Success, percentage, isChrarging
    
    def dpi_stage_info(self, StageNo=6):
        Success, response = send_command(self.device, protocal_cmd.get_dpi_stage_info(self.profileID, StageNo))

        DPI_list = []
        for i in range(StageNo):
            dpi = (response[8 + 4*i] * 256) + (response[9 + 4*i])
            DPI_list.append(dpi)

        return Success, DPI_list
    
    def dpi_stage(self):
        Success, response = send_command(self.device, protocal_cmd.get_dpi_stage(self.profileID))

        CurrentStage = response[7]

        return Success, CurrentStage

    def dev_firmware_ver(self):
        Success, response = send_command(self.device, protocal_cmd.get_dev_firmware_ver())

        FirmwareVer = ""
        for i in range(7, 11):
            FirmwareVer += f"{response[i]:02d}."

        return Success, FirmwareVer[:-1]
    
    def dongle_firmware_ver(self):
        Success, response = send_command(self.device, protocal_cmd.get_dongle_firmware_ver())

        FirmwareVer = ""
        for i in range(7, 11):
            FirmwareVer += f"{response[i]:02d}."

        return Success, FirmwareVer[:-1]
    
    def lift_off_dist(self):
        Success, response = send_command(self.device, protocal_cmd.get_lift_off(self.profileID))

        if self.profileID == -1:
            dist = response[6]
        else:
            dist = response[7]

        if dist == 0x87:
            dist = 0.7

        return Success, dist
    
    def PID(self):
        Success, response = send_command(self.device, protocal_cmd.get_device_pid())

        pid = response[10] * 256 + response[11]     
        return Success, pid
    
    def polling_rate(self):  # NOTE: need to oberseve source code
        Polling_rates = {
            8 : 125,
            4 : 250,
            2 : 500,
            1 : 1000,
            16 : 1000,
            32 : 2000,
            64 : 4000,
            128 : 8000
        }

        packet = protocal_cmd.get_polling_rate(self.profileID)
        Success, response = send_command(self.device, packet)

        for _ in range(5):
            if not packet[5] != response[4] and packet[6] != response[5]:
                self.device.send_feature_report(packet)
                time.sleep(0.03)
                response = self.device.get_feature_report(2, 65)
            else:
                break

        if self.profileID == -1:
            PollingRateIdx = response[6]
        else:
            PollingRateIdx = response[7]

        if Success == True:
            PollingRate = Polling_rates[PollingRateIdx]
        else:
            PollingRate = None

        return Success, PollingRate
    
    def motion_sync(self):
        Success, response = send_command(self.device, protocal_cmd.get_motion_sync(self.profileID))
        if self.profileID == -1:
            isEnabled = response[6]
        else:
            isEnabled = response[7]

        return Success, isEnabled
    
    def pairing(self):
        Success, response = send_command(self.device, protocal_cmd.get_paired())
        isPaired = response[6]

        return Success, isPaired
    
    def ripple_control(self):
        Success, response = send_command(self.device, protocal_cmd.get_ripple_contol(self.profileID))
        
        if self.profileID == -1:
            isEnabled = response[6]
        else:
            isEnabled = response[7]

        return Success, isEnabled
    
    def sleep_time(self):
        Success, response = send_command(self.device, protocal_cmd.get_sleep(self.profileID))
        
        if self.profileID == -1:
            Stime = (response[6] * 256) + response[7]
        else:
            Stime = (response[7] * 256) + response[8]

        return Success, Stime

class SET:
    def __init__(self, dev, profileID):
        self.profileID = profileID
        self.device = dev

    def angle_snap(self, enable):
        Success, _ = send_command(self.device, protocal_cmd.set_angle_snap(enable, self.profileID))

        return Success
    
    def debounce_time(self, DebounceTime):
        Success, _ = send_command(self.device, protocal_cmd.set_debounce(DebounceTime, self.profileID))

        return Success
    
    def dongle_LED(self, enable):
        Success, _ = send_command(self.device, protocal_cmd.set_dongle_LED(enable, self.profileID))

        return Success
    
    def dpi_stage_info(self, StageNo, DPIValue): # NOTE: need to finsih this
        Success, _ = send_command(self.device, protocal_cmd.set_dpi_stage_info(StageNo, DPIValue, self.profileID))

        return Success
    
    def dpi_stage(self, CurrentStage):
        Success, _ = send_command(self.device, protocal_cmd.set_dpi_stage(self.profileID, CurrentStage))

        return Success
    
    def lift_off_dist(self, dist):

        if dist == 0.7:
            dist = 0x87
        else:
            dist = int(dist)

        Success, _ = send_command(self.device, protocal_cmd.set_lift_off(self.profileID, dist))

        return Success
    
    def polling_rate(self, PollingRate): 
        Polling_rates = {
            125 : 8,
            250 : 4,
            500 : 2,
            1000 : 1,
            2000 : 32,
            4000 : 64,
            8000 : 128
        }
        Success, _ = send_command(self.device, protocal_cmd.set_polling_rate(Polling_rates[PollingRate], self.profileID))
        
        return Success
    
    def motion_sync(self, enable):
        Success, _ = send_command(self.device, protocal_cmd.set_motion_sync(enable, self.profileID))

        return Success
    
    def pairing(self, isPaired):
        Success, _ = send_command(self.device, protocal_cmd.pair_to_device(isPaired))

        return Success
    
    def ripple_control(self, enable):
        Success, _ = send_command(self.device, protocal_cmd.set_ripple_contol(enable, self.profileID))

        return Success
    
    def sleep_time(self, Stime):
        Success, _ = send_command(self.device, protocal_cmd.set_sleep(Stime, self.profileID))

        return Success
    
    def reset_profile(self):
        Success, _ = send_command(self.device, protocal_cmd.reset_profile(self.profileID), NoGetFeature=True)

        return Success
    
    def reset_defaults(self):
        Success, _ = send_command(self.device, protocal_cmd.reset_defaults(), NoGetFeature=True)

        return Success