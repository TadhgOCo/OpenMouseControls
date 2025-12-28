import mouse_hid
import argparse


description = """
A CLI tool designed to communicate with ATTACKSHARK Mice.
For the list of compatable devices look at the README
"""

PossiblePropertiesList = [
    "GetAngleSnap",
    "SetAngleSnap",
    "GetBattery",
    "GetDebounce",
    "SetDebounce",
    "SetDongleLED",
    "GetDongleLED",
    "SetDpiStage",
    "GetDpiStage",
    "SetDpiStageInfo",
    "GetDpiStageInfo",
    "GetDevFirmwareVer",
    "GetDongleFirmwareVer",
    "GetLiftOff",
    "SetLiftOff",
    "GetDevicePid",
    "SetMotionSync",
    "GetMotionSync",
    "PairToDevice",
    "GetPaired",
    "SetPollingRate",
    "GetPollingRate",
    "ResetDefaults",
    "ResetProfile",
    "GetRippleContol",
    "SetRippleContol",
    "GetSleep",
    "SetSleep"
]

PossibleProperties = ""
for Property in PossiblePropertiesList:
    PossibleProperties += Property + ", "

def main(args):
    device = mouse_hid.find_device()

    if not device:
        print("No compatible device found.")
        exit(1)

    Property  = args.Property
    value = int(args.value)
    verbose = int(args.verbose)

    try:
        MouseProperties = mouse_hid.properties(device, 1, verbose)
    except Exception as e:
        if mouse_hid.check_perms() == False:
            options = ["y", "n", ""]
            while True:
                UsrOutput = input("No Premissions, would you like to install them? (Y/n): ")
                InstallPerms = UsrOutput.strip().lower()
                if InstallPerms in options:
                    break

            if InstallPerms == "n":
                print("Cannot Connect to Mouse:\nNo Premissions")
                device.close()
                exit(1)
            
            else:
                try:
                    mouse_hid.install_perms()
                except Exception as e:
                    print(f"Cannot Connect to Mouse:\nPremission Install Failed:\n{e}")
                    device.close()
                    exit(1)

            if mouse_hid.check_perms() == False:
                print("Premission Installed Successfully")
            else:
                print(f"Cannot Connect to Mouse:\nPremission Install Failed\nTry install maually from udev folder on GitHub")
                device.close()
                exit(1)

    PropertiesDict = {
        "GetAngleSnap": MouseProperties.get.angle_snap,
        "SetAngleSnap": MouseProperties.set.angle_snap,

        "GetBattery": MouseProperties.get.battery,

        "GetDebounce": MouseProperties.get.debounce_time,
        "SetDebounce": MouseProperties.set.debounce_time,

        "SetDongleLED": MouseProperties.set.dongle_LED,
        "GetDongleLED": MouseProperties.get.dongle_LED,

        "SetDpiStage": MouseProperties.set.dpi_stage,
        "GetDpiStage": MouseProperties.get.dpi_stage,

        "SetDpiStageInfo": lambda value: MouseProperties.set.dpi_stage_info(6, value),
        "GetDpiStageInfo": lambda : MouseProperties.get.dpi_stage_info(6),

        "GetDevFirmwareVer": MouseProperties.get.dev_firmware_ver,
        "GetDongleFirmwareVer": MouseProperties.get.dongle_firmware_ver,

        "GetLiftOff": MouseProperties.get.lift_off_dist,
        "SetLiftOff": MouseProperties.set.lift_off_dist,

        "GetDevicePid": MouseProperties.get.PID,

        "SetMotionSync": MouseProperties.set.motion_sync,
        "GetMotionSync": MouseProperties.get.motion_sync,

        "PairToDevice": MouseProperties.set.pairing,
        "GetPaired": MouseProperties.get.pairing,

        "SetPollingRate": MouseProperties.set.polling_rate,
        "GetPollingRate": MouseProperties.get.polling_rate,

        "ResetDefaults": MouseProperties.set.reset_defaults,
        "ResetProfile": MouseProperties.set.reset_profile,

        "GetRippleContol": MouseProperties.get.ripple_control,
        "SetRippleContol": MouseProperties.set.ripple_control,

        "GetSleep": MouseProperties.get.sleep_time,
        "SetSleep": MouseProperties.set.sleep_time
    }

    if Property not in PropertiesDict.keys():
        print("Invalid Properties:\nTry $python mousecli.py -h")
        device.close()
        exit(1)

    command = PropertiesDict[Property]

    if "Get" in Property:
        out = command()
    else:
        out = command(value)

    if type(out) == tuple:
        print(f"\nSuccess: {out[0]}\nValue: {out[1]}")
    else:
        print(f"\nSuccess: {out}\n")

    device.close()

def cmdline_args():
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    
    parser.add_argument("Property",
                   help=f"The Property you want to change, Possible Values Include: {PossibleProperties}")
    
    
    parser.add_argument("--value", type=int, default=0,
                   help="The Value you want to change the Property to")
    
    parser.add_argument("-v", "--verbose", type=int, default=0,
                   help="verbose output")

    parsed = parser.parse_args()
    return parsed

if __name__ == '__main__':
    try:
        args = cmdline_args()
        main(args)
    except Exception as e:
        print(f"Try $python mousecli.py DongleLED 1, {e}")