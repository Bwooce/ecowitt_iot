"""Support for Ecowitt IoT switches."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MODEL_AC1100
from .coordinator import EcowittDataUpdateCoordinator
from .models import EcowittDeviceDescription

_LOGGER = logging.getLogger(__name__)


@dataclass
class EcowittSwitchEntityDescription(SwitchEntityDescription):
    """Describes Ecowitt switch entity."""

    status_key: str = ""


SWITCH_DESCRIPTIONS = {
    MODEL_AC1100: EcowittSwitchEntityDescription(
        key="power_switch",
        name="Power",
        status_key="ac_status",
    ),
    1: EcowittSwitchEntityDescription(  # WFC01
        key="valve_switch",
        name="Valve",
        status_key="water_status",
    ),
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ecowitt switch based on a config entry."""
    coordinator: EcowittDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        EcowittSwitch(
            coordinator=coordinator,
            device=device,
            description=SWITCH_DESCRIPTIONS[device.model],
        )
        for device in coordinator.devices
        if device.model in SWITCH_DESCRIPTIONS
    )


class EcowittSwitch(CoordinatorEntity[EcowittDataUpdateCoordinator], SwitchEntity):
    """Representation of an Ecowitt switch."""

    entity_description: EcowittSwitchEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: EcowittDataUpdateCoordinator,
        device: EcowittDeviceDescription,
        description: EcowittSwitchEntityDescription,
    ) -> None:
        """Initialize the switch."""
        super().__init__(coordinator)
        self.entity_description = description
        self._device = device
        self._attr_unique_id = f"{DOMAIN}_{device.device_id}_{description.key}"
        self._attr_entity_id = f"{DOMAIN}.{description.name.lower().replace(' ', '_')}_{description.key}"
        self._attr_device_info = device.device_info
        self._attr_name = description.name

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self._device.device_id in self.coordinator.data
            and len(self.coordinator.data[self._device.device_id].get("command", []))
            > 0
        )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        try:
            await self.coordinator.set_device_state(self._device.device_id, True)
            # Force an immediate update after state change
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error("Error turning on device %s: %s", self._device.device_id, err)
            raise

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        try:
            await self.coordinator.set_device_state(self._device.device_id, False)
            # Force an immediate update after state change
            await self.coordinator.async_request_refresh()
        except Exception as err:
            _LOGGER.error(
                "Error turning off device %s: %s", self._device.device_id, err
            )
            raise

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        try:
            device_data = self.coordinator.data[self._device.device_id]["command"][0]
            _LOGGER.debug("Switch status check - Device data: %s", device_data)

            if self._device.model == 1:  # WFC01
                if not any(
                    key in device_data
                    for key in ("water_status", "always_on", "water_running")
                ):
                    # No status fields at all: unknown, not "off".
                    return None
                # Check both water_status and always_on
                water_status = device_data.get("water_status", 0)
                always_on = device_data.get("always_on", 0)
                is_running = device_data.get("water_running", 0)

                _LOGGER.debug(
                    "WFC01 state check - water_status: %s, always_on: %s, water_running: %s",
                    water_status,
                    always_on,
                    is_running,
                )

                # Return true if either condition is met
                return bool(water_status) or bool(is_running)
            else:  # AC1100
                return bool(device_data.get("ac_status", 0))
        except (KeyError, IndexError) as err:
            _LOGGER.error("Error getting switch state: %s", err)
            return None
