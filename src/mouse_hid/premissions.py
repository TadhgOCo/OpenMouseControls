import subprocess
import hid
import os
import sys

TARGET_VENDORS = [0x258A, 0x373E] 

def install_perms():
    if sys.platform == "win32":
        return

    cwd = os.getcwd()
    print(f"{cwd}/udev/install-udev.sh", cwd)
    subprocess.run([
        "pkexec",
        "/usr/bin/sh",
        f"{cwd}/udev/install-udev.sh",
        cwd
    ])

def check_perms():
    if sys.platform == "win32":
        return True

    for d in hid.enumerate():
        if d["vendor_id"] not in TARGET_VENDORS:
            continue
        try:
            h = hid.Device(path=d["path"])
            h.close()
            return True
        except OSError:
            pass
    return False