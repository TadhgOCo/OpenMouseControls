#!/bin/sh
cp 99-mouse-hid.rules /etc/udev/rules.d/
udevadm control --reload-rules
udevadm trigger

pip install -e .