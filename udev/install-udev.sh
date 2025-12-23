#!/bin/sh
cp "$1/udev/99-mouse-hid.rules" /etc/udev/rules.d/
udevadm control --reload-rules
udevadm trigger