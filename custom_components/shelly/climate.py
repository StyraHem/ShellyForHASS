"""
Shelly platform for the climate component.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""

import logging

from homeassistant.components.climate import ClimateEntity
from homeassistant.const import (
    ATTR_TEMPERATURE,
    PRECISION_TENTHS,
    TEMP_CELSIUS
)
try:
    from homeassistant.components.climate.const import HVACMode, ClimateEntityFeature
    MODE_HEAT = HVACMode.HEAT
    MODE_OFF = HVACMode.OFF
    FEATURES = ClimateEntityFeature.TARGET_TEMPERATURE
except :
    #deprecated as of Home Assistant 2022.5
    from homeassistant.components.climate.const import CURRENT_HVAC_OFF, CURRENT_HVAC_HEAT, SUPPORT_TARGET_TEMPERATURE
    MODE_HEAT = CURRENT_HVAC_HEAT
    MODE_OFF = CURRENT_HVAC_OFF
    FEATURES = SUPPORT_TARGET_TEMPERATURE

from homeassistant.helpers.dispatcher import async_dispatcher_connect
from .const import *

# from .sensor import ShellySensor
from .device import ShellyDevice
from .block import ShellyBlock

from typing import Any

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Shelly climate dynamically."""
    async def async_discover_climate(dev, instance):
        """Discover and add a discovered sensor."""
        async_add_entities([ShellyClimate(dev, instance)])

    async_dispatcher_connect(
        hass,
        "shelly_new_climate",
        async_discover_climate
    )

class ShellyClimate(ShellyDevice, ClimateEntity):
    _attr_hvac_mode = MODE_HEAT
    _attr_hvac_modes = [MODE_HEAT] #MODE_OFF, 
    _attr_max_temp = 30
    _attr_min_temp = 5
    _attr_supported_features = FEATURES
    _attr_target_temperature_step = PRECISION_TENTHS
    _attr_temperature_unit = TEMP_CELSIUS

    """Representation of an Shelly Switch."""
    def __init__(self, dev, instance):
        """Initialize an ShellyClimate."""
        ShellyDevice.__init__(self, dev, instance)
        self.entity_id = "climate" + self.entity_id
        self._state = None
        self._master_unit = True

    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        pass

    def set_temperature(self, **kwargs: Any) -> None:
        if (temp := kwargs.get(ATTR_TEMPERATURE)) is None:
            return
        self._dev.set_target_temp(temp)

    async def async_update(self) -> None:
        self._attr_target_temperature = self._dev.info_values.get("target_temperature")
        self._attr_current_temperature = self._dev.info_values.get("temperature")
        self._attr_available = True
        self._attr_hvac_mode = MODE_HEAT
        self._attr_icon = "mdi:radiator"
    
