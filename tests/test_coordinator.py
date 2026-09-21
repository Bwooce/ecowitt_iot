"""Tests for the Ecowitt IoT coordinator fetch behaviour."""

from __future__ import annotations

from typing import Any
from unittest.mock import Mock

import pytest
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant

from custom_components.ecowitt_iot.coordinator import EcowittDataUpdateCoordinator
from custom_components.ecowitt_iot.models import EcowittDeviceDescription

DEVICE_ID = "12345"

REAL_READING = (
    '{"command":[{"model":1,"id":12345,"water_status":0,"water_total":"1501.855",'
    '"flow_velocity":"0.00","water_temp":"19.7","timeutc":1600000000}]}'
)


class _FakeResponse:
    """Minimal stand-in for an aiohttp response."""

    def __init__(self, text: str) -> None:
        self._text = text

    async def text(self) -> str:
        return self._text


class _FakePost:
    """Minimal stand-in for the context manager returned by session.post()."""

    def __init__(self, text: str) -> None:
        self._text = text

    async def __aenter__(self) -> _FakeResponse:
        return _FakeResponse(self._text)

    async def __aexit__(self, *args: Any) -> bool:
        return False


@pytest.fixture
def device() -> EcowittDeviceDescription:
    """Return a WFC01 test device."""
    return EcowittDeviceDescription(device_id=DEVICE_ID, model=1, name="Test Device")


@pytest.fixture
async def coordinator(hass: HomeAssistant, device) -> EcowittDataUpdateCoordinator:
    """Create a coordinator whose transport is patched per test."""
    entry = Mock()
    entry.data = {CONF_HOST: "gateway.invalid"}
    return EcowittDataUpdateCoordinator(hass=hass, entry=entry, devices=[device])


def _respond_with(coordinator: EcowittDataUpdateCoordinator, text: str) -> None:
    """Make the coordinator's session answer every request with text."""
    coordinator.session = Mock(post=Mock(return_value=_FakePost(text)))


async def test_valid_reading_is_returned_and_cached(coordinator) -> None:
    """A JSON reading is returned to the entities and remembered."""
    _respond_with(coordinator, REAL_READING)

    data = await coordinator._async_update_data()

    payload = data[DEVICE_ID]["command"][0]
    assert payload["water_total"] == "1501.855"
    # Remembered so a later "200 OK" poll can serve it instead of failing.
    assert coordinator._last_good_data[DEVICE_ID]["command"][0] == payload


async def test_bare_200_ok_without_history_publishes_nothing(coordinator) -> None:
    """A "200 OK" with no previous reading must not fabricate one.

    The gateway answers "200 OK" when it has not read the device yet. Serving
    placeholder values in that case (water_total "0.00") is indistinguishable
    from a real report: a utility_meter helper downstream books the return to
    the real total as consumption, and a flow/leak binary_sensor clears while
    the leak is still there. The device is therefore left out of the poll
    result, which is what makes its entities report unavailable.
    """
    _respond_with(coordinator, "200 OK")

    data = await coordinator._async_update_data()

    # No reading published for the device ...
    assert DEVICE_ID not in data
    # ... and none invented and kept for the next poll either.
    assert coordinator._last_good_data == {}


async def test_bare_200_ok_replays_the_last_real_reading(coordinator) -> None:
    """With a reading already seen, a "200 OK" poll replays it unchanged."""
    _respond_with(coordinator, REAL_READING)
    good = await coordinator._async_update_data()

    _respond_with(coordinator, "200 OK")
    replayed = await coordinator._async_update_data()

    assert replayed == good
    assert replayed[DEVICE_ID]["command"][0]["water_total"] == "1501.855"


async def test_payload_without_device_fields_is_not_a_reading(coordinator) -> None:
    """A well-formed envelope with none of the device fields is not a reading.

    The gateway answers `{"command":[{}]}` (or with only the envelope keys)
    while it has not read the device. Parsing succeeds, so caching it would
    serve that empty payload to the entities, whose own defaults turn it into
    0 litres and a closed valve.
    """
    _respond_with(coordinator, '{"command":[{}]}')

    data = await coordinator._async_update_data()

    assert DEVICE_ID not in data
    assert coordinator._last_good_data == {}


async def test_payload_without_device_fields_replays_the_last_reading(
    coordinator,
) -> None:
    """With a real reading already seen, an empty payload does not poison it."""
    _respond_with(coordinator, REAL_READING)
    good = await coordinator._async_update_data()

    _respond_with(coordinator, '{"command":[{"timeutc": 1600000001}]}')
    replayed = await coordinator._async_update_data()

    assert replayed == good
    assert replayed[DEVICE_ID]["command"][0]["water_total"] == "1501.855"

