"""
Shelly platform for the switch component.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""

import logging

try:
    from homeassistant.components.switch import SwitchEntity
except:
    from homeassistant.components.switch import \
        SwitchDevice as SwitchEntity
from homeassistant.helpers.entity import ToggleEntity
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from .const import *

# from .sensor import ShellySensor
from .device import ShellyDevice
from .block import ShellyBlock

_LOGGER = logging.getLogger(__name__)

# def setup_platform(hass, _config, add_devices, discovery_info=None):
#    """Setup the Shelly Switch platform."""
#
#    if 'firmware' in discovery_info:
#        block = get_block_from_hass(hass, discovery_info)
#        add_devices([ShellyFirmwareUpdate(block, hass)])
#        return
#
#    dev = get_device_from_hass(hass, discovery_info)
#    add_devices([ShellySwitch(dev, hass)])

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Shelly switch dynamically."""
    async def async_discover_switch(dev, instance):
        """Discover and add a discovered sensor."""
        if isinstance(dev, dict):
            if 'firmware' in dev:
                block = dev['block']
                update_switch = getattr(block, 'firmware_switch', None)
                if not update_switch:
                    async_add_entities(
                        [ShellyFirmwareUpdate(block, instance)])
            return
        async_add_entities([ShellySwitch(dev, instance)])

    async_dispatcher_connect(
        hass,
        "shelly_new_switch",
        async_discover_switch
    )

class ShellySwitch(ShellyDevice, SwitchEntity):
    """Representation of an Shelly Switch."""
    def __init__(self, dev, instance):
        """Initialize an ShellySwitch."""
        ShellyDevice.__init__(self, dev, instance)
        self._state = None
        self._master_unit = True
        self.update()

    @property
    def is_on(self):
        """Get device state"""
        return self._state

    def turn_on(self, **_kwargs):
        """Turn on device"""
        self._dev.turn_on()
        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **_kwargs):
        """Turn off device"""
        self._dev.turn_off()
        self._state = False
        self.schedule_update_ha_state()

    def update(self):
        """Fetch new state data for this switch."""
        self._state = self._dev.state

class ShellyFirmwareUpdate(ShellyBlock, SwitchEntity):
    """Representation of a script entity."""

    def __init__(self, block, instance):
        block.firmware_switch = self
        self._updating = False
        ShellyBlock.__init__(self, block, instance, "_firmware_update")
        self.entity_id = "switch" + self.entity_id
        self._master_unit = False

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def name(self):
        return "Upgrade firmware " + ShellyBlock.name.fget(self)

    @property
    def device_state_attributes(self):
        attrs = super().device_state_attributes
        attrs[ATTRIBUTE_LATEST_FW] = \
            self._block.info_values[ATTRIBUTE_LATEST_FW]
        attrs[ATTRIBUTE_FW] = \
            self._block.info_values[ATTRIBUTE_FW]
        return attrs

    @property
    def is_on(self):
        """Return true if is on."""
        return self._updating

    async def async_turn_on(self, **_kwargs):
        """Trig the firmware update"""
        self._updating = True
        self.schedule_update_ha_state()
        await self.hass.async_add_executor_job(self._block.update_firmware)

    async def async_turn_off(self, **_kwargs):
        """Do nothing"""
        self.schedule_update_ha_state()

    def remove(self):
        self._block.firmware_switch = None
        ShellyBlock.remove(self)
