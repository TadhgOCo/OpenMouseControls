# src/mouse_hid/__init__.py

__version__ = "0.0.1"

from .angle_snap import get_angle_snap, set_angle_snap
from .battery import get_battery
from .debounce import get_debounce, set_debounce
from .dongle import set_dongle_LED, get_dongle_LED
from .dpi import set_dpi_stage_info, get_dpi_stage, set_dpi_stage, get_dpi_stage_info
from .firmware_version import get_dev_firmware_ver, get_dongle_firmware_ver
#from .button import get_button, set_button
from .lift_off import get_lift_off, set_lift_off
from .pid import get_device_pid
from .motion_sync import set_motion_sync, get_motion_sync
from .pair_status import pair_to_device, get_paired
from .polling import set_polling_rate, get_polling_rate
from .profile import reset_defaults, reset_profile
from .ripple import get_ripple_contol, set_ripple_contol
from .sleep_time import get_sleep, set_sleep

__all__ = [
    "get_angle_snap",
    "set_angle_snap",
    "get_battery",
    "get_debounce",
    "set_debounce",
    "set_dongle_LED",
    "set_dpi_stage",
    "get_dpi_stage",
    "set_dpi_stage_info",
    "get_dpi_stage_info",
    "get_dev_firmware_ver",
    "get_dongle_firmware_ver",
    "get_lift_off",
    "set_lift_off",
    "get_device_pid",
    "get_dongle_LED",
    "set_motion_sync",
    "get_motion_sync",
    "pair_to_device",
    "get_paired",
    "set_polling_rate",
    "get_polling_rate",
    "reset_defaults",
    "reset_profile",
    "get_ripple_contol",
    "set_ripple_contol",
    "get_sleep",
    "set_sleep"
]
