"""Test the Ecowitt IoT switch platform."""

from __future__ import annotations

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.const import STATE_OFF, STATE_ON
from homeassistant.core import HomeAssistant

from custom_components.ecowitt_iot.const import DOMAIN
from custom_components.ecowitt_iot.switch import async_setup_entry

pytestmark = pytest.mark.asyncio

ENTITY_ID = "switch.test_device_valve"


@pytest.fixture
def mock_switch_entry(hass: HomeAssistant) -> MockConfigEntry:
    """Create a config entry with one WFC01."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_entry",
        data={
            "devices": [
                {
                    "id": "12345",
                    "model": 1,
                    "version": "1.0.5",
                    "nickname": "Test Device",
                }
            ]
        },
    )
    entry.add_to_hass(hass)
    return entry


async def _setup(hass, coordinator, adder, entry):
    """Register the coordinator and set up the switch platform."""
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await async_setup_entry(hass, entry, adder.async_add_entities)
    await hass.async_block_till_done()
    assert len(adder.entities) == 1, "Expected 1 switch"
    return adder.entities[0]


async def test_switch_setup(
    hass: HomeAssistant,
    mock_coordinator,
    mock_add_entities,
    mock_switch_entry,
) -> None:
    """The valve switch is created and reports off."""
    await _setup(
        hass, mock_coordinator, mock_add_entities, mock_switch_entry
    )

    state = hass.states.get(ENTITY_ID)
    assert state is not None
    assert state.state == STATE_OFF


async def test_switch_turn_on(
    hass: HomeAssistant,
    mock_coordinator,
    mock_add_entities,
    mock_switch_entry,
) -> None:
    """Turning on sends quick_run and reflects the new reading."""
    switch = await _setup(
        hass, mock_coordinator, mock_add_entities, mock_switch_entry
    )

    await switch.async_turn_on()
    await hass.async_block_till_done()
    mock_coordinator.set_device_state.assert_awaited_once_with(
        "12345", True
    )

    mock_coordinator.data["12345"]["command"][0].update(
        {"water_status": 1, "water_running": 1}
    )
    await switch.async_update_ha_state(True)
    await hass.async_block_till_done()

    assert hass.states.get(ENTITY_ID).state == STATE_ON


async def test_switch_turn_off(
    hass: HomeAssistant,
    mock_coordinator,
    mock_add_entities,
    mock_switch_entry,
) -> None:
    """Turning off sends quick_stop and reflects the new reading."""
    mock_coordinator.data["12345"]["command"][0].update(
        {"water_status": 1, "water_running": 1}
    )
    switch = await _setup(
        hass, mock_coordinator, mock_add_entities, mock_switch_entry
    )
    assert hass.states.get(ENTITY_ID).state == STATE_ON

    await switch.async_turn_off()
    await hass.async_block_till_done()
    mock_coordinator.set_device_state.assert_awaited_once_with(
        "12345", False
    )

    mock_coordinator.data["12345"]["command"][0].update(
        {"water_status": 0, "water_running": 0}
    )
    await switch.async_update_ha_state(True)
    await hass.async_block_till_done()

    assert hass.states.get(ENTITY_ID).state == STATE_OFF
