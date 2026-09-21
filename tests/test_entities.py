"""Entity-level tests: a payload without the device fields must not become 0/off.

The coordinator refuses to publish a payload that carries none of the device's
own fields, but the entities are the last line of defence: their own `.get(...)`
defaults are what turned an empty payload into "0 litres consumed" and
"valve closed" in the field.
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest
from homeassistant.const import UnitOfTemperature

from custom_components.ecowitt_iot.binary_sensor import EcowittBinarySensor, WFC01_BINARY_SENSORS
from custom_components.ecowitt_iot.coordinator import EcowittDataUpdateCoordinator
from custom_components.ecowitt_iot.models import EcowittDeviceDescription
from custom_components.ecowitt_iot.sensor import EcowittSensor, WFC01_SENSORS
from custom_components.ecowitt_iot.switch import SWITCH_DESCRIPTIONS, EcowittSwitch

DEVICE_ID = "12345"


def _coordinator(payload: dict) -> Mock:
    """Return a mock coordinator serving one payload, optionally empty."""
    coordinator = Mock(spec=EcowittDataUpdateCoordinator)
    coordinator.devices = [
        EcowittDeviceDescription(device_id=DEVICE_ID, model=1, name="Test Device")
    ]
    coordinator.data = {DEVICE_ID: {"command": [payload]}}
    return coordinator


def _description(key: str):
    return next(d for d in WFC01_SENSORS if d.key == key)


def _sensor(payload: dict, key: str) -> EcowittSensor:
    return EcowittSensor(
        coordinator=_coordinator(payload),
        device=EcowittDeviceDescription(device_id=DEVICE_ID, model=1, name="Test Device"),
        description=_description(key),
        temp_unit=UnitOfTemperature.CELSIUS,
    )


def _switch(payload: dict) -> EcowittSwitch:
    return EcowittSwitch(
        coordinator=_coordinator(payload),
        device=EcowittDeviceDescription(device_id=DEVICE_ID, model=1, name="Test Device"),
        description=SWITCH_DESCRIPTIONS[1],
    )


def _binary(payload: dict) -> EcowittBinarySensor:
    description = next(d for d in WFC01_BINARY_SENSORS if d.key == "leak")
    return EcowittBinarySensor(
        coordinator=_coordinator(payload),
        device=EcowittDeviceDescription(device_id=DEVICE_ID, model=1, name="Test Device"),
        description=description,
    )


REAL_PAYLOAD = {
    "water_status": 1,
    "water_total": "1501.855",
    "flow_velocity": "0.00",
    "water_temp": "19.7",
    "warning": 2,  # bit 1 = no_water
    "wfc01batt": 5,
}


# --- sensors ----------------------------------------------------------------
def test_sensor_reports_the_real_reading() -> None:
    assert _sensor(REAL_PAYLOAD, "total_water").native_value == 1501.855
    assert _sensor(REAL_PAYLOAD, "flow_rate").native_value == 0.0


def test_sensor_reports_none_when_the_field_is_missing() -> None:
    """No water_total in the payload is not the same as zero litres."""
    assert _sensor({}, "total_water").native_value is None
    assert _sensor({"water_status": 0}, "total_water").native_value is None
    assert _sensor({"timeutc": 1600000000}, "flow_rate").native_value is None


def test_sensor_still_reports_a_measured_zero() -> None:
    """A real zero in the payload is data, not an absence."""
    assert _sensor({"water_total": "0.00"}, "total_water").native_value == 0.0


# --- switch -----------------------------------------------------------------
def test_switch_reflects_the_real_status() -> None:
    assert _switch(REAL_PAYLOAD).is_on is True
    assert _switch({"water_status": 0, "always_on": 0, "water_running": 0}).is_on is False


def test_switch_is_unknown_when_there_are_no_status_fields() -> None:
    """An empty payload must not be reported as 'valve closed'."""
    assert _switch({}).is_on is None
    assert _switch({"water_total": "1501.855"}).is_on is None


# --- binary sensors ---------------------------------------------------------
def test_binary_sensor_reflects_the_warning_bits() -> None:
    assert _binary(REAL_PAYLOAD).is_on is False  # water_leak is bit 0, clear here
    assert _binary({"warning": 1}).is_on is True  # bit 0 set = leak


def test_binary_sensor_is_unknown_without_the_warning_byte() -> None:
    """Warning bits all reading clear is a safety statement, not a default."""
    assert _binary({}).is_on is None
    assert _binary({"water_total": "1501.855"}).is_on is None


def test_binary_sensor_still_reports_a_clear_warning_byte() -> None:
    """A real warning byte of 0 still means 'no leak', not 'unknown'."""
    assert _binary({"warning": 0}).is_on is False
