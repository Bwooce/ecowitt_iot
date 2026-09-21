"""Support for Ecowitt IoT binary sensors."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN, EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MODEL_AC1100
from .coordinator import EcowittDataUpdateCoordinator
from .models import EcowittDeviceDescription

_LOGGER = logging.getLogger(__name__)


@dataclass
class EcowittBinarySensorDescription(BinarySensorEntityDescription):
    """Describes an Ecowitt binary sensor."""

    bit_position: int = 0
    inverted: bool = False  # Added to dataclass


AC1100_BINARY_SENSORS = [
    EcowittBinarySensorDescription(
        key="leak_current",
        name="Leak Current",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        bit_position=0,
    ),
    EcowittBinarySensorDescription(
        key="no_load",
        name="No Load",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        bit_position=1,
    ),
    EcowittBinarySensorDescription(
        key="low_current",
        name="Low Current",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        bit_position=2,
    ),
    EcowittBinarySensorDescription(
        key="overload",
        name="Overload",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        bit_position=3,
    ),
    EcowittBinarySensorDescription(
        key="relay_abnormal",
        name="Relay Problem",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        bit_position=4,
    ),
    EcowittBinarySensorDescription(
        key="offline",
        name="Device Connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
        bit_position=7,
        inverted=True,
    ),
]

WFC01_BINARY_SENSORS = [
    EcowittBinarySensorDescription(
        key="leak",
        name="Water Leak",
        device_class=BinarySensorDeviceClass.MOISTURE,
        entity_category=EntityCategory.DIAGNOSTIC,
        bit_position=0,
    ),
    EcowittBinarySensorDescription(
        key="no_water",
        name="No Water",
        device_class=BinarySensorDeviceClass.PROBLEM,
        entity_category=EntityCategory.DIAGNOSTIC,
        bit_position=1,
    ),
    EcowittBinarySensorDescription(
        key="temp_low",
        name="Temperature Low",
        device_class=BinarySensorDeviceClass.COLD,
        entity_category=EntityCategory.DIAGNOSTIC,
        bit_position=2,
    ),
    EcowittBinarySensorDescription(
        key="temp_high",
        name="Temperature High",
        device_class=BinarySensorDeviceClass.HEAT,
        entity_category=EntityCategory.DIAGNOSTIC,
        bit_position=3,
    ),
    EcowittBinarySensorDescription(
        key="low_battery",
        name="Battery Low",
        device_class=BinarySensorDeviceClass.BATTERY,
        entity_category=EntityCategory.DIAGNOSTIC,
        bit_position=4,
    ),
    EcowittBinarySensorDescription(
        key="offline",
        name="Device Connected",
        device_class=BinarySensorDeviceClass.CONNECTIVITY,
        entity_category=EntityCategory.DIAGNOSTIC,
        bit_position=7,
        inverted=True,
    ),
]


class EcowittBinarySensor(
    CoordinatorEntity[EcowittDataUpdateCoordinator], BinarySensorEntity
):
    """Representation of an Ecowitt binary sensor."""

    entity_description: EcowittBinarySensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: EcowittDataUpdateCoordinator,
        device: EcowittDeviceDescription,
        description: EcowittBinarySensorDescription,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._device = device
        self._attr_unique_id = f"{DOMAIN}_{device.device_id}_{description.key}"
        self._attr_device_info = device.device_info

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        try:
            device_data = self.coordinator.data[self._device.device_id]["command"][0]
            if "warning" not in device_data:
                # The warning byte is an assertion of safety (leak, no water,
                # temperature, battery, connectivity). Absent is unknown, not
                # "all clear".
                _LOGGER.debug(
                    "No warning byte in payload for device %s", self._device.device_id
                )
                return None

            warning_byte = device_data.get("warning", 0)

            _LOGGER.debug(
                "Device %s warning byte: %s (raw). Checking bit %d for %s",
                self._device.device_id,
                bin(warning_byte),
                self.entity_description.bit_position,
                self.entity_description.key,
            )

            # Calculate bit value
            bit_value = bool(warning_byte & (1 << self.entity_description.bit_position))

            # Invert if needed
            result = not bit_value if self.entity_description.inverted else bit_value

            _LOGGER.debug(
                "Device %s sensor %s bit value: %s (inverted: %s, final: %s)",
                self._device.device_id,
                self.entity_description.key,
                bit_value,
                self.entity_description.inverted,
                result,
            )

            return result

        except (KeyError, IndexError) as err:
            _LOGGER.error(
                "Error getting warning bit for device %s sensor %s: %s",
                self._device.device_id,
                self.entity_description.key,
                err,
            )
            return None

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return (
            super().available
            and self._device.device_id in self.coordinator.data
            and len(self.coordinator.data[self._device.device_id].get("command", []))
            > 0
        )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ecowitt binary sensors based on a config entry."""
    coordinator: EcowittDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities: list[EcowittBinarySensor] = []

    for device in coordinator.devices:
        sensors = (
            AC1100_BINARY_SENSORS
            if device.model == MODEL_AC1100
            else WFC01_BINARY_SENSORS
        )
        for description in sensors:
            entities.append(
                EcowittBinarySensor(
                    coordinator=coordinator,
                    device=device,
                    description=description,
                )
            )
            _LOGGER.debug(
                "Added binary sensor %s for device %s",
                description.key,
                device.device_id,
            )

    async_add_entities(entities)


# async def async_added_to_hass(self) -> None:
#    """Handle entity which will be added."""
#    await super().async_added_to_hass()
#    if (state := await self.async_get_last_state()) is not None:
#        if state.state not in (STATE_UNKNOWN, STATE_UNAVAILABLE):
#            self._attr_native_value = state.state
