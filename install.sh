#!/bin/bash

if [ "$EUID" -ne 0 ]; then 
  echo "Please run the script as root (use sudo [script name])"
  exit
fi

echo "Installing Permissions..."
if [ -f "udev/99-mouse-hid.rules" ]; then
    cp udev/99-mouse-hid.rules /etc/udev/rules.d/
    udevadm control --reload-rules
    udevadm trigger
    echo "Permissions Installed!"
else
    echo "Error: udev rule file not found."
fi

read -p "Would you like to install the Python Package (Y/n): " isInstalling

if [[ "$isInstalling" =~ ^[Yy]$ ]]; then
    echo "Installing Python Package..."

    if [ -f "requirments.txt" ]; then
        python3 -m pip install -r requirments.txt
    fi

    python3 -m pip install -e .
    echo "Finished Installing Python Package"
fi

echo "Done!"