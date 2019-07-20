"""
Shelly platform for the switch component.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""

import logging

from homeassistant.components.switch import SwitchDevice
from homeassistant.helpers.entity import ToggleEntity

# from .sensor import ShellySensor
from . import (ShellyDevice, get_device_from_hass,
               ShellyBlock, get_block_from_hass)

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, _config, add_devices, discovery_info=None):
    """Setup the Shelly Switch platform."""

    if 'firmware' in discovery_info:
        block = get_block_from_hass(hass, discovery_info)
        add_devices([ShellyFirmwareUpdate(block, hass)])
        return

    dev = get_device_from_hass(hass, discovery_info)
    add_devices([ShellySwitch(dev, hass)])

class ShellySwitch(ShellyDevice, SwitchDevice):
    """Representation of an Shelly Switch."""

    def __init__(self, dev, hass):
        """Initialize an ShellySwitch."""
        ShellyDevice.__init__(self, dev, hass)
        self._state = None
        self.update()

    @property
    def current_power_w(self):
        """Return the current power usage in W."""
        if hasattr(self._dev, 'sensorValues'):
            return self._dev.sensorValues['consumption']
        return None

    @property
    def today_energy_kwh(self):
        """Return the today total energy usage in kWh."""
        return None

    @property
    def is_on(self):
        """Get device state"""
        return self._state

    def turn_on(self, **_kwargs):
        """Turn on device"""
        self._dev.turn_on()

    def turn_off(self, **_kwargs):
        """Turn off device"""
        self._dev.turn_off()

    def update(self):
        """Fetch new state data for this switch."""
        self._state = self._dev.state

class ShellyFirmwareUpdate(ShellyBlock, SwitchDevice):
    """Representation of a script entity."""

    def __init__(self, block, hass):
        ShellyBlock.__init__(self, block, hass, "_firmware_update")
        self.entity_id = "switch" + self.entity_id
        self._name = "Upgrade firmware " + self._name
        self._updating = False
        block.firmware_switch = self

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def is_on(self):
        """Return true if is on."""
        return self._updating

    async def async_turn_on(self, **_kwargs):
        """Trig the firmware update"""
        self._updating = True
        self.schedule_update_ha_state(False)
        self._block.update_firmware()
            
    async def async_turn_off(self, **_kwargs):
        """Do nothing"""
        self.schedule_update_ha_state(False)

    def remove(self):
        self._block.firmware_switch = None
        ShellyBlock.remove(self)
