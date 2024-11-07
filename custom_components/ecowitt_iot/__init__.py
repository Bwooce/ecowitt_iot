"""The Ecowitt IoT integration."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN
from .coordinator import EcowittDataUpdateCoordinator
from .models import EcowittDeviceDescription

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.BINARY_SENSOR,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Ecowitt IoT from a config entry."""
    try:
        devices = [
            EcowittDeviceDescription(
                device_id=str(device["id"]),
                model=device["model"],
                name=device.get("nickname"),
                sw_version=str(device.get("version")),
            )
            for device in entry.data.get("devices", [])
        ]

        coordinator = EcowittDataUpdateCoordinator(
            hass=hass,
            entry=entry,
            devices=devices,
        )

        await coordinator.async_config_entry_first_refresh()
    except asyncio.TimeoutError as ex:
        raise ConfigEntryNotReady(
            f"Timeout connecting to device at {entry.data[CONF_HOST]}"
        ) from ex
    except Exception as ex:
        raise ConfigEntryNotReady(
            f"Failed to connect to device at {entry.data[CONF_HOST]}: {str(ex)}"
        ) from ex

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
    