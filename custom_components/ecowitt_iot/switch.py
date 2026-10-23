"""Support for Ecowitt IoT switches."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.components.switch import (
    SwitchEntity,
    SwitchEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import entity_platform
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
import voluptuous as vol

from .const import (
    ATTR_DURATION,
    ATTR_VOLUME,
    DOMAIN,
    MAX_VOLUME_LITRES,
    MODEL_AC1100,
    MODEL_WFC01,
    SERVICE_RUN_BY_VOLUME,
    SERVICE_SET_POWER_TIMER,
    SERVICE_SET_VALVE_TIMER,
)
from .coordinator import EcowittDataUpdateCoordinator
from .models import EcowittDeviceDescription

_LOGGER = logging.getLogger(__name__)


@dataclass
class EcowittSwitchEntityDescription(SwitchEntityDescription):
    """Describes Ecowitt switch entity."""

    status_key: str = ""


# Device-side timers: the gateway stops the output itself, so a run
# bounded here survives Home Assistant going away mid-cycle.
TIMER_SCHEMA = {
    vol.Required(ATTR_DURATION): vol.All(
        vol.Coerce(int), vol.Range(min=1, max=1440)
    ),
}
VOLUME_SCHEMA = {
    vol.Required(ATTR_VOLUME): vol.All(
        vol.Coerce(int), vol.Range(min=1, max=MAX_VOLUME_LITRES)
    ),
}

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
    coordinator: EcowittDataUpdateCoordinator = hass.data[DOMAIN][
        entry.entry_id
    ]

    async_add_entities(
        EcowittSwitch(
            coordinator=coordinator,
            device=device,
            description=SWITCH_DESCRIPTIONS[device.model],
        )
        for device in coordinator.devices
        if device.model in SWITCH_DESCRIPTIONS
    )

    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        SERVICE_SET_VALVE_TIMER,
        TIMER_SCHEMA,
        "async_run_for_duration",
    )
    platform.async_register_entity_service(
        SERVICE_SET_POWER_TIMER,
        TIMER_SCHEMA,
        "async_run_for_duration",
    )
    platform.async_register_entity_service(
        SERVICE_RUN_BY_VOLUME,
        VOLUME_SCHEMA,
        "async_run_for_volume",
    )


class EcowittSwitch(
    CoordinatorEntity[EcowittDataUpdateCoordinator], SwitchEntity
):
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
        self._attr_unique_id = (
            f"{DOMAIN}_{device.device_id}_{description.key}"
        )
        self._attr_entity_id = f"{DOMAIN}.{description.name.lower().replace(' ', '_')}_{description.key}"
        self._attr_device_info = device.device_info
        self._attr_name = description.name

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self._device.device_id in self.coordinator.data
            and len(
                self.coordinator.data[self._device.device_id].get(
                    "command", []
                )
            )
            > 0
        )

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the entity on."""
        try:
            await self.coordinator.set_device_state(
                self._device.device_id, True
            )
        except Exception as err:
            _LOGGER.error(
                "Error turning on device %s: %s",
                self._device.device_id,
                err,
            )
            raise

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the entity off."""
        try:
            await self.coordinator.set_device_state(
                self._device.device_id, False
            )
        except Exception as err:
            _LOGGER.error(
                "Error turning off device %s: %s",
                self._device.device_id,
                err,
            )
            raise

    async def async_run_for_duration(self, duration: int) -> None:
        """Turn on with a device-side timer (minutes)."""
        try:
            await self.coordinator.run_for_duration(
                self._device.device_id, duration
            )
        except ValueError as err:
            raise HomeAssistantError(str(err)) from err

    async def async_run_for_volume(self, volume: int) -> None:
        """Open a WFC01 valve until `volume` litres have passed."""
        if self._device.model != MODEL_WFC01:
            raise HomeAssistantError(
                "run_by_volume is only supported on the WFC01 valve"
            )
        try:
            await self.coordinator.run_for_volume(
                self._device.device_id, volume
            )
        except ValueError as err:
            raise HomeAssistantError(str(err)) from err

    @property
    def is_on(self) -> bool | None:
        """Return true if the switch is on."""
        try:
            device_data = self.coordinator.data[self._device.device_id][
                "command"
            ][0]
            _LOGGER.debug(
                "Switch status check - Device data: %s", device_data
            )

            # water_status / ac_status is the valve or relay state. On a
            # live WFC01 water_running lags water_status by about a
            # second after quick_stop, so OR-ing it in left the switch
            # showing on for a whole poll interval after turning off.
            return bool(
                device_data.get(self.entity_description.status_key, 0)
            )
        except (KeyError, IndexError) as err:
            _LOGGER.error("Error getting switch state: %s", err)
            return None
