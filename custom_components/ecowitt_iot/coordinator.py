"""Coordinator for Ecowitt IoT integration."""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Any

import async_timeout
from aiohttp import ClientError, ClientTimeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.util import dt as dt_util

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN
from .models import EcowittDeviceDescription

_LOGGER = logging.getLogger(__name__)


class EcowittDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching Ecowitt IoT data."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        devices: list[EcowittDeviceDescription],
    ) -> None:
        """Initialize coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.config_entry = entry
        self.devices = devices
        self.host = entry.data[CONF_HOST]
        self.session = aiohttp_client.async_get_clientsession(hass)
        self._last_good_data: dict[str, Any] = {}

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via API."""
        try:
            async with async_timeout.timeout(30):
                return await self._fetch_data()
        except asyncio.TimeoutError as err:
            raise UpdateFailed("Timeout communicating with API") from err
        except ClientError as err:
            raise UpdateFailed(
                f"Error communicating with API: {err}"
            ) from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err

    async def _fetch_data(self) -> dict[str, Any]:
        """Fetch data from API."""
        data = {}
        for device in self.devices:
            try:
                device_data = await self._fetch_device_data(device)
                if device_data:
                    data[device.device_id] = device_data
            except Exception as err:
                _LOGGER.error(
                    "Error fetching data for device %s: %s",
                    device.device_id,
                    err,
                )
                # Use last known good data if available
                if device.device_id in self._last_good_data:
                    data[device.device_id] = self._last_good_data[
                        device.device_id
                    ]
        return data

    async def _fetch_device_data(
        self, device: EcowittDeviceDescription
    ) -> dict[str, Any]:
        """Fetch data for a specific device."""
        url = f"http://{self.host}/parse_quick_cmd_iot"
        payload = {
            "command": [
                {
                    "cmd": "read_device",
                    "id": int(device.device_id),
                    "model": device.model,
                }
            ]
        }

        try:
            _LOGGER.debug("Sending payload to %s: %s", url, payload)

            timeout = ClientTimeout(total=10)
            async with self.session.post(
                url, json=payload, timeout=timeout
            ) as response:
                text = await response.text()
                text = text.strip(" %\n\r")

                _LOGGER.debug("Received response text: %s", text)

                if text == "200 OK":
                    # A bare "200 OK" means the gateway accepted the
                    # command but has no reading for this device yet.
                    # Never synthesise readings here: a fabricated
                    # water_total of 0 reads as a meter rollover to
                    # TOTAL_INCREASING consumers such as utility_meter.
                    if device.device_id in self._last_good_data:
                        _LOGGER.debug(
                            "No new reading for device %s, keeping last",
                            device.device_id,
                        )
                        return self._last_good_data[device.device_id]

                    _LOGGER.debug(
                        "No reading yet for device %s, leaving unavailable",
                        device.device_id,
                    )
                    return {}

                try:
                    data = json.loads(text)
                    # Store this as last known good data
                    self._last_good_data[device.device_id] = data
                    _LOGGER.debug(
                        "Stored good data for device %s: %s",
                        device.device_id,
                        data,
                    )
                    return data
                except json.JSONDecodeError as err:
                    _LOGGER.error(
                        "Error parsing JSON for device %s: %s. "
                        "Response: %s",
                        device.device_id,
                        err,
                        text,
                    )
                    raise UpdateFailed("Invalid response format") from err

        except Exception as err:
            _LOGGER.error(
                "Error fetching data for device %s: %s",
                device.device_id,
                err,
            )
            raise

    async def set_device_state(self, device_id: str, state: bool) -> None:
        """Set device state."""
        device = next(
            (d for d in self.devices if d.device_id == device_id), None
        )
        if not device:
            raise ValueError(f"Device {device_id} not found")

        _LOGGER.debug("Setting device %s state to %s", device_id, state)

        url = f"http://{self.host}/parse_quick_cmd_iot"
        if state:
            payload = {
                "command": [
                    {
                        "cmd": "quick_run",
                        "on_type": 0,
                        "off_type": 0,
                        "always_on": 1,
                        "on_time": 0,
                        "off_time": 0,
                        "val_type": 0,
                        "val": 0,
                        "id": int(device_id),
                        "model": device.model,
                    }
                ]
            }
        else:
            payload = {
                "command": [
                    {
                        "cmd": "quick_stop",
                        "id": int(device_id),
                        "model": device.model,
                    }
                ]
            }

        try:
            _LOGGER.debug("Sending command to %s: %s", url, payload)

            timeout = ClientTimeout(total=10)
            async with self.session.post(
                url, json=payload, timeout=timeout
            ) as response:
                text = await response.text()
                text = text.strip(" %\n\r")
                _LOGGER.debug("Received response: %s", text)

                if text != "200 OK":
                    raise UpdateFailed(
                        f"Failed to set device state: {text}"
                    )

                await asyncio.sleep(1)
                await self.async_request_refresh()

        except Exception as err:
            _LOGGER.error("Error setting device state: %s", err)
            raise UpdateFailed(
                f"Failed to set device state: {err}"
            ) from err

    def get_device_last_update(self, device_id: str) -> datetime | None:
        """Get the last update time for a device."""
        try:
            device_data = self.data[device_id]["command"][0]
            timestamp = device_data.get("timeutc", 0)
            if timestamp:
                return dt_util.utc_from_timestamp(int(timestamp))
        except (KeyError, ValueError, TypeError):
            pass
        return None
