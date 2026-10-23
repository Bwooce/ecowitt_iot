"""Test the Ecowitt IoT data coordinator."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant

from custom_components.ecowitt_iot.const import DOMAIN
from custom_components.ecowitt_iot.coordinator import (
    EcowittDataUpdateCoordinator,
)
from custom_components.ecowitt_iot.models import EcowittDeviceDescription

pytestmark = pytest.mark.asyncio

DEVICE_ID = "12345"

REAL_READING = {
    "command": [
        {
            "model": 1,
            "id": 12345,
            "water_status": 0,
            "warning": 0,
            "water_total": "1501.855",
            "flow_velocity": "0.00",
            "timeutc": 1700000000,
        }
    ]
}


def _mock_session(responses: list[str]) -> MagicMock:
    """Build a session whose post() yields the given bodies in turn."""
    session = MagicMock()
    bodies = iter(responses)

    def _post(*_args, **_kwargs):
        response = MagicMock()
        response.text = AsyncMock(return_value=next(bodies))
        ctx = MagicMock()
        ctx.__aenter__ = AsyncMock(return_value=response)
        ctx.__aexit__ = AsyncMock(return_value=False)
        return ctx

    session.post = _post
    return session


def _coordinator(
    hass: HomeAssistant, session: MagicMock
) -> EcowittDataUpdateCoordinator:
    """Create a coordinator wired to a fake aiohttp session."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        entry_id="test_entry",
        data={CONF_HOST: "192.0.2.1", "devices": []},
    )
    entry.add_to_hass(hass)
    device = EcowittDeviceDescription(device_id=DEVICE_ID, model=1)
    with patch(
        "custom_components.ecowitt_iot.coordinator"
        ".aiohttp_client.async_get_clientsession",
        return_value=session,
    ):
        return EcowittDataUpdateCoordinator(hass, entry, [device])


async def test_bare_ok_before_any_reading_leaves_device_absent(
    hass: HomeAssistant,
) -> None:
    """A '200 OK' with no prior reading must not fabricate data."""
    coordinator = _coordinator(hass, _mock_session(["200 OK"]))

    data = await coordinator._async_update_data()

    assert data == {}


async def test_bare_ok_after_reading_keeps_last_good_data(
    hass: HomeAssistant,
) -> None:
    """A '200 OK' after a real reading must return that reading."""
    session = _mock_session([json.dumps(REAL_READING), "200 OK"])
    coordinator = _coordinator(hass, session)

    first = await coordinator._async_update_data()
    second = await coordinator._async_update_data()

    assert first[DEVICE_ID] == REAL_READING
    assert second[DEVICE_ID] == REAL_READING
    # The total must never collapse to zero between two polls, as that
    # reads as a meter rollover to total_increasing consumers.
    assert (
        second[DEVICE_ID]["command"][0]["water_total"]
        == first[DEVICE_ID]["command"][0]["water_total"]
    )


async def test_trailing_percent_is_stripped(hass: HomeAssistant) -> None:
    """The gateway appends a stray '%' to JSON bodies; it is removed."""
    body = json.dumps(REAL_READING) + "%"
    coordinator = _coordinator(hass, _mock_session([body]))

    data = await coordinator._async_update_data()

    assert data[DEVICE_ID] == REAL_READING


def _capture_session() -> tuple[MagicMock, list[dict]]:
    """Session that answers '200 OK' and records every posted payload."""
    session = MagicMock()
    sent: list[dict] = []

    def _post(_url, json=None, **_kwargs):
        sent.append(json)
        response = MagicMock()
        response.text = AsyncMock(return_value="200 OK")
        ctx = MagicMock()
        ctx.__aenter__ = AsyncMock(return_value=response)
        ctx.__aexit__ = AsyncMock(return_value=False)
        return ctx

    session.post = _post
    return session, sent


async def test_turn_on_sends_unbounded_quick_run(
    hass: HomeAssistant,
) -> None:
    """A plain turn-on is always_on=1 with no quantity."""
    session, sent = _capture_session()
    coordinator = _coordinator(hass, session)
    with patch("asyncio.sleep", new=AsyncMock()):
        await coordinator.set_device_state(DEVICE_ID, True)

    cmd = sent[0]["command"][0]
    assert cmd["cmd"] == "quick_run"
    assert cmd["always_on"] == 1
    assert cmd["val_type"] == 0 and cmd["val"] == 0
    assert cmd["id"] == 12345 and cmd["model"] == 1


async def test_run_for_duration_sends_minute_timer(
    hass: HomeAssistant,
) -> None:
    """A timed run is always_on=0, val_type=1 (minutes), val=N."""
    session, sent = _capture_session()
    coordinator = _coordinator(hass, session)
    with patch("asyncio.sleep", new=AsyncMock()):
        await coordinator.run_for_duration(DEVICE_ID, 15)

    cmd = sent[0]["command"][0]
    assert cmd["cmd"] == "quick_run"
    assert cmd["always_on"] == 0
    assert cmd["val_type"] == 1
    assert cmd["val"] == 15


async def test_run_for_volume_sends_litre_quantity(
    hass: HomeAssistant,
) -> None:
    """A volume run is always_on=0, val_type=3 (litres), val=N."""
    session, sent = _capture_session()
    coordinator = _coordinator(hass, session)
    with patch("asyncio.sleep", new=AsyncMock()):
        await coordinator.run_for_volume(DEVICE_ID, 20)

    cmd = sent[0]["command"][0]
    assert cmd["always_on"] == 0
    assert cmd["val_type"] == 3
    assert cmd["val"] == 20


async def test_run_for_volume_rejects_ac1100(hass: HomeAssistant) -> None:
    """Volume runs are refused for the AC1100."""
    session, sent = _capture_session()
    coordinator = _coordinator(hass, session)
    coordinator.devices[0].model = 2

    with pytest.raises(ValueError):
        await coordinator.run_for_volume(DEVICE_ID, 20)
    assert sent == []
