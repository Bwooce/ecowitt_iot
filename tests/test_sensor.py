"""Test the Ecowitt IoT sensor platform."""

from __future__ import annotations

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.const import (
    CONF_TEMPERATURE_UNIT,
    PERCENTAGE,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant

from custom_components.ecowitt_iot.const import DOMAIN
from custom_components.ecowitt_iot.sensor import (
    WFC01_SENSORS,
    async_setup_entry,
)

pytestmark = pytest.mark.asyncio


@pytest.fixture
def sensor_entry(hass: HomeAssistant) -> MockConfigEntry:
    """Create a config entry with one WFC01."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_entry",
        data={
            CONF_TEMPERATURE_UNIT: UnitOfTemperature.CELSIUS,
            "devices": [
                {
                    "id": "12345",
                    "model": 1,
                    "version": "1.0.5",
                    "nickname": "Test Device",
                }
            ],
        },
    )
    entry.add_to_hass(hass)
    return entry


async def test_sensor_creation(
    hass: HomeAssistant, mock_coordinator, mock_add_entities, sensor_entry
) -> None:
    """Every WFC01 sensor is created and reports the coordinator data."""
    hass.data.setdefault(DOMAIN, {})[
        sensor_entry.entry_id
    ] = mock_coordinator

    await async_setup_entry(
        hass, sensor_entry, mock_add_entities.async_add_entities
    )
    await hass.async_block_till_done()

    assert len(mock_add_entities.entities) == len(WFC01_SENSORS)

    state = hass.states.get("sensor.test_device_water_temperature")
    assert state is not None, "Water temperature sensor not found"
    assert state.state == "20.0"
    assert (
        state.attributes["unit_of_measurement"] == UnitOfTemperature.CELSIUS
    )

    state = hass.states.get("sensor.test_device_flow_rate")
    assert state is not None, "Flow rate sensor not found"
    assert state.state == "1.5"

    state = hass.states.get("sensor.test_device_battery")
    assert state is not None, "Battery sensor not found"
    assert state.state == "80"
    assert state.attributes["unit_of_measurement"] == PERCENTAGE


async def test_sensor_unavailable_without_device_data(
    hass: HomeAssistant, mock_coordinator, mock_add_entities, sensor_entry
) -> None:
    """A device with no reading in coordinator data is unavailable."""
    mock_coordinator.data = {}
    hass.data.setdefault(DOMAIN, {})[
        sensor_entry.entry_id
    ] = mock_coordinator

    await async_setup_entry(
        hass, sensor_entry, mock_add_entities.async_add_entities
    )
    await hass.async_block_till_done()

    state = hass.states.get("sensor.test_device_total_water")
    assert state is not None
    assert state.state == "unavailable"
