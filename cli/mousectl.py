import mouse_hid
import time

device = mouse_hid.find_device()

if not device:
    print("No compatible device found.")
    exit(1)

properties = mouse_hid.properties(device, 1)

#properties.set.polling_rate(2000)
print("GET DATA")
#print(properties.get.polling_rate())

#print(properties.set.sleep_time(322))
#print(properties.get.sleep_time())
#time.sleep(5)
#properties.set.reset_profile()

exit(0)
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
    print(key, data[key])
    time.sleep(0.01)
    i += 1



while True:
    #_, stage = properties.get.dpi_stage()
    #_, stages = properties.get.dpi_stage_info()
    #print(stages[stage-1])

    #print(properties.get.motion_sync())
    #print(properties.get.angle_snap())
    #print(properties.get.ripple_control())
    #print(properties.get.dongle_LED())

    #print(properties.get.polling_rate())

    time.sleep(1)

# Widgets.py
"""
Searching for device...
Found device: R6 Mouse 2.4G (0x373e:0x22)
Success: Device acknowledged command (0xA1).
Starting
Success: Device acknowledged command (0xA1).
Angle Snap 0
Success: Device acknowledged command (0xA1).
Motion Sync 0
Success: Device acknowledged command (0xA1).
Ripple Control 0
Success: Device acknowledged command (0xA1).
Dongle LED 0
Success: Device acknowledged command (0xA1).
DPI Level 2400
Success: Device acknowledged command (0xA1).
Polling Rate 500
Success: Device acknowledged command (0xA1).
Debounce Time 3
Success: Device acknowledged command (0xA1).
Lift-off Distance 1
Success: Device acknowledged command (0xA1).
Sleep Timer 15
Success: Device acknowledged command (0xA1).
"""

# This Script
"""
Searching for device...
Found device: R6 Mouse 2.4G (0x373e:0x22)
Success: Device acknowledged command (0xA1).
Starting
Success: Device acknowledged command (0xA1).
Angle Snap 0
Success: Device acknowledged command (0xA1).
Motion Sync 0
Success: Device acknowledged command (0xA1).
Ripple Control 0
Success: Device acknowledged command (0xA1).
Dongle LED 0
Success: Device acknowledged command (0xA1).
DPI Level 1600
Success: Device acknowledged command (0xA1).
Polling Rate 1000
Success: Device acknowledged command (0xA1).
Debounce Time 1
Success: Device acknowledged command (0xA1).
Lift-off Distance 135
Success: Device acknowledged command (0xA1).
Sleep Timer 167
"""