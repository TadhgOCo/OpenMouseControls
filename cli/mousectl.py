import mouse_hid
import time

device = mouse_hid.find_device()

if not device:
    print("No compatible device found.")
    exit(1)

properties = mouse_hid.properties(device, 1)

#properties.set.dpi_stage(2)
#properties.set.dongle_LED(0)

while True:
    #_, stage = properties.get.dpi_stage()
    #_, stages = properties.get.dpi_stage_info()
    #print(stages[stage-1])

    print(properties.get.motion_sync())
    print(properties.get.angle_snap())
    print(properties.get.ripple_control())
    print(properties.get.dongle_LED())

    time.sleep(1)