"""Button entities for Acaia scales."""
from collections.abc import Callable, Coroutine
from dataclasses import dataclass
from typing import Any

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .acaiaclient import AcaiaClient
from .const import DOMAIN
from .entity import AcaiaEntity, AcaiaEntityDescription


@dataclass
class AcaiaButtonEntityDescriptionMixin:
    """Mixin for Acaia Button entities."""

    async_press_fn: Callable[[AcaiaClient], Coroutine[Any, Any, None]]


@dataclass
class AcaiaButtonEntityDescription(
    ButtonEntityDescription, AcaiaEntityDescription, AcaiaButtonEntityDescriptionMixin
):
    """Description for Acaia Button entities."""


BUTTONS: tuple[AcaiaButtonEntityDescription, ...] = (
    AcaiaButtonEntityDescription(
        key="tare",
        translation_key="tare",
        icon="mdi:scale-balance",
        unique_id_fn=lambda scale: f"{scale.mac}_tare_button",
        async_press_fn=lambda scale: scale.tare(),
    ),
    AcaiaButtonEntityDescription(
        key="reset_timer",
        translation_key="reset_timer",
        icon="mdi:timer-refresh",
        unique_id_fn=lambda scale: f"{scale.mac}_reset_button",
        async_press_fn=lambda scale: scale.reset_timer(),
    ),
    AcaiaButtonEntityDescription(
        key="start_stop",
        translation_key="start_stop",
        icon="mdi:timer-play",
        unique_id_fn=lambda scale: f"{scale.mac}_start_stop_button",
        async_press_fn=lambda scale: scale.start_stop_timer(),
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up button entities and services."""

    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities(
        [AcaiaButton(coordinator, description) for description in BUTTONS]
    )


class AcaiaButton(AcaiaEntity, ButtonEntity):
    """Representation of a Acaia Button."""

    entity_description: AcaiaButtonEntityDescription

    async def async_press(self) -> None:
        """Handle the button press."""
        await self.entity_description.async_press_fn(self._scale)
        self.async_write_ha_state()
