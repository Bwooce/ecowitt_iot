"""DataUpdateCoordinator for Ecowitt IoT."""
from __future__ import annotations

import asyncio
import json
import logging
from datetime import timedelta
from typing import Any

import aiohttp
from aiohttp import ClientError
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    DOMAIN,
    DEFAULT_SCAN_INTERVAL,
)
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
        self._host = entry.data[CONF_HOST]
        self._session = async_get_clientsession(hass)

    async def _async_update_data(self) -> dict[str, Any]:
        """Update data via API."""
        try:
            async with async_timeout.timeout(10):
                return await self._fetch_data()
        except asyncio.TimeoutError as err:
            raise UpdateFailed("Timeout communicating with API") from err
        except ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
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
        return data

    async def _fetch_device_data(self, device: EcowittDeviceDescription) -> dict[str, Any]:
        """Fetch data for a specific device."""
        url = f"http://{self._host}/parse_quick_cmd_iot"
        payload = {
            "command": [{
                "cmd": "read_device",
                "id": device.device_id,
                "model": device.model
            }]
        }
        
        async with self._session.post(url, json=payload) as response:
            text = await response.text()
            # Clean the response
            text = text.strip(' %\n\r')
            
            try:
                return json.loads(text)
            except json.JSONDecodeError as err:
                _LOGGER.error(
                    "Error parsing JSON for device %s: %s. Response: %s",
                    device.device_id,
                    err,
                    text,
                )
                raise UpdateFailed("Invalid response format") from err