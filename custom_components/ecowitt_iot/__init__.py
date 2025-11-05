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

    # DEPRECATION WARNING
    _LOGGER.warning(
        "⚠️ DEPRECATION WARNING ⚠️ The ecowitt_iot integration is deprecated. "
        "Please migrate to the official Ecowitt integration: "
        "https://github.com/Ecowitt/ha-ecowitt-iot - "
        "See MIGRATION.md for instructions."
    )

    # Create persistent notification
    hass.components.persistent_notification.async_create(
        title="⚠️ Ecowitt IoT Integration Deprecated",
        message=(
            "The **ecowitt_iot** integration is deprecated and will no longer receive updates.\n\n"
            "Please migrate to the **official Ecowitt integration**:\n"
            "https://github.com/Ecowitt/ha-ecowitt-iot\n\n"
            "📖 See the [MIGRATION.md](https://github.com/Bwooce/ecowitt_iot/blob/main/MIGRATION.md) "
            "guide for step-by-step instructions.\n\n"
            "The official integration provides the same functionality with company support."
        ),
        notification_id="ecowitt_iot_deprecation",
    )

    try:
        _LOGGER.debug("Setting up entry with data: %s", entry.data)

        devices_data = entry.data.get("devices", [])
        if not devices_data:
            _LOGGER.error("No devices found in config entry")
            raise ConfigEntryNotReady("No devices configured")

        devices = []
        for device_data in devices_data:
            try:
                device = EcowittDeviceDescription(
                    device_id=str(device_data["id"]),
                    model=int(device_data["model"]),
                    name=device_data.get("nickname"),
                    sw_version=device_data.get(
                        "version"
                    ),  # This will now be properly formatted
                )
                devices.append(device)
                _LOGGER.debug(
                    "Added device: id=%s, model=%s, version=%s",
                    device.device_id,
                    device.model_name,
                    device.sw_version,
                )
            except KeyError as err:
                _LOGGER.error("Missing required field for device: %s", err)
                continue

        if not devices:
            raise ConfigEntryNotReady("No valid devices configured")

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
        _LOGGER.exception("Failed to setup integration")
        raise ConfigEntryNotReady(
            f"Failed to connect to device at {entry.data[CONF_HOST]}: {str(ex)}"
        ) from ex

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True
