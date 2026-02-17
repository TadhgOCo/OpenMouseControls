# src/mouse_hid/__init__.py

__version__ = "0.1.0"

from .device import find_device, SUFFIX_LIST
from .protocal import properties
from .premissions import install_perms, check_perms

__all__ = [
    "find_device",
    "set",
    "get",
    "properties",
    "install_perms",
    "check_perms",
    "SUFFIX_LIST"
]
