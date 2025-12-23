import subprocess
import hid
import os


def install_perms():
    cwd = os.getcwd()
    print(f"{cwd}/udev/install-udev.sh", cwd)
    subprocess.run([
        "pkexec",
        "/usr/bin/sh",
        f"{cwd}/udev/install-udev.sh",
        cwd
    ])

TARGET_VENDORS = [0x258A, 0x373E] 


def check_perms():
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