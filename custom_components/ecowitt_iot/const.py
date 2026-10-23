"""Constants for the Ecowitt IoT integration."""

from datetime import timedelta
from typing import Final

DOMAIN: Final = "ecowitt_iot"

# Configuration
CONF_DEVICE_ID: Final = "device_id"
CONF_MODEL: Final = "model"

# Defaults
DEFAULT_NAME: Final = "Ecowitt IoT"
DEFAULT_SCAN_INTERVAL: Final = 30  # seconds

# Device Models
MODEL_AC1100: Final = 2
MODEL_WFC01: Final = 1

# Device Status
STATUS_OFFLINE: Final = "offline"
STATUS_ONLINE: Final = "online"

# Attributes
ATTR_DEVICE_ID: Final = "device_id"
ATTR_MODEL: Final = "model"
ATTR_WARNING: Final = "warning"

# Error/Warning Bits
ERROR_BITS_AC1100: Final[dict[int, str]] = {
    0: "leak_current",
    1: "no_load",
    2: "low_current",
    3: "overload",
    4: "relay_abnormal",
    7: "offline",
}

ERROR_BITS_WFC01: Final[dict[int, str]] = {
    0: "leak",
    1: "no_water",
    2: "temp_low",
    3: "temp_high",
    4: "low_battery",
    7: "offline",
}

# Turndown: this integration is superseded by Ecowitt's official one.
OFFICIAL_INTEGRATION_URL: Final = (
    "https://github.com/Ecowitt/ha-ecowitt-iot"
)
DEPRECATION_ISSUE_ID: Final = "deprecated_superseded_by_official"

# quick_run val_type values (unit of "val"), per the local IoT API
VAL_TYPE_SECONDS: Final = 0
VAL_TYPE_MINUTES: Final = 1
VAL_TYPE_HOURS: Final = 2
VAL_TYPE_LITRES: Final = 3  # WFC01 only
VAL_TYPE_FOREVER: Final = -1  # sentinel: always_on=1, no quantity

# Services
SERVICE_SET_VALVE_TIMER: Final = "set_valve_timer"
SERVICE_SET_POWER_TIMER: Final = "set_power_timer"
SERVICE_RUN_BY_VOLUME: Final = "run_by_volume"
ATTR_DURATION: Final = "duration"
ATTR_VOLUME: Final = "volume"
