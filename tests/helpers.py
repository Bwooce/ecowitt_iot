"""Test helpers for Ecowitt IoT tests."""

from __future__ import annotations

import logging
from collections.abc import Iterable

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)


class MockEntityAdder:
    """Stand-in for the platform's async_add_entities callback.

    Home Assistant calls async_add_entities synchronously (it is a plain
    callback that schedules work), so this must be a regular function.
    Entities are recorded immediately; adding them to the state machine
    is scheduled on the event loop and completes once the test awaits
    hass.async_block_till_done().
    """

    def __init__(self, hass: HomeAssistant):
        """Initialize the helper."""
        self.hass = hass
        self.entities: list[Entity] = []

    def async_add_entities(
        self, entities: Iterable[Entity], update_before_add: bool = False
    ) -> None:
        """Record the entities and schedule adding them to HA."""
        entities = list(entities)
        self.entities.extend(entities)
        for entity in entities:
            self.hass.async_create_task(self._add_entity(entity))

    async def _add_entity(self, entity: Entity) -> None:
        """Attach one entity to hass and write its initial state."""
        entity.hass = self.hass
        if not entity.entity_id:
            domain = entity.__class__.__module__.rsplit(".", 1)[-1]
            device_slug = entity._device.name.lower().replace(" ", "_")
            name_slug = str(entity.name).lower().replace(" ", "_")
            entity.entity_id = f"{domain}.{device_slug}_{name_slug}"
        await entity.async_added_to_hass()
        await entity.async_update_ha_state(force_refresh=True)
        _LOGGER.debug(
            "Added entity %s with state %s", entity.entity_id, entity.state
        )
