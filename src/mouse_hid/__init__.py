# src/mouse_hid/__init__.py

__version__ = "0.1.0"

from .device import find_device
from .protocal import properties
from .errors import MouseHIDError
from .premissions import install_perms, check_perms

__all__ = [
    "find_device",
    "set",
    "get",
    "properties",
    "MouseHIDError",
    "install_perms",
    "check_perms"
]
