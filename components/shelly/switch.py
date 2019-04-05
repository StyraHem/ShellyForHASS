"""
Shelly platform for the switch component.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""

import logging

from homeassistant.components.switch import SwitchDevice

# from .sensor import ShellySensor
from . import ShellyDevice, get_device_from_hass

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Shelly Switch platform."""
    dev = get_device_from_hass(hass, discovery_info)
    add_devices([ShellySwitch(dev, hass)])

class ShellySwitch(ShellyDevice, SwitchDevice):
    """Representation of an Shelly Switch."""

    def __init__(self, dev, hass):
        """Initialize an ShellySwitch."""
        ShellyDevice.__init__(self, dev, hass)
        self._state = None
        self.update()

    def _updated(self):
        """Receive events when the switch state changed (by mobile,
        switch etc)"""
        self.schedule_update_ha_state(True)

    @property
    def current_power_w(self):
        """Return the current power usage in W."""
        if hasattr(self._dev, 'sensorValues'):
            return self._dev.sensorValues['watt']
        return None

    @property
    def today_energy_kwh(self):
        """Return the today total energy usage in kWh."""
        return None

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        self._dev.turn_on()

    def turn_off(self, **kwargs):
        self._dev.turn_off()

    def update(self):
        """Fetch new state data for this switch."""
        self._state = self._dev.state
