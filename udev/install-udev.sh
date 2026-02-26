#!/bin/bash

if [ "$EUID" -ne 0 ]; then 
  echo "Please run the script as root (use sudo [script name])"
  exit
fi

echo "Installing Permissions..."
if [ -f "udev/99-mouse-hid.rules" ]; then
    cp "$1/udev/99-mouse-hid.rules" /etc/udev/rules.d/
    udevadm control --reload-rules
    udevadm trigger
    echo "Permissions Installed!"
else
    echo "Error: udev rule file not found."
fi

echo "Done!"