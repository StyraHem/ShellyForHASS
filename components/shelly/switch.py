"""
Shelly platform for the switch component.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""

import logging
#from .sensor import ShellySensor, SENSOR_TYPE_POWER
from . import ShellyDevice
from homeassistant.components.switch import SwitchDevice

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Shelly Switch platform."""
    dataKey = discovery_info['dataKey']
    dev = hass.data[dataKey]
    add_devices([ShellySwitch(dev, hass)])
    hass.data[dataKey]=None

class ShellySwitch(ShellyDevice, SwitchDevice):
    """Representation of an Shelly Switch."""

    def __init__(self, dev, hass):
        """Initialize an ShellySwitch."""
        ShellyDevice.__init__(self, dev, hass)
        self._state = None
        self.update()

    def _updated(self):
        """Receive events when the switch state changed (by mobile, switch etc)"""
        if self.entity_id is not None:
            state = self._hass.states.get(self.entity_id)
            if state is not None:
                self._hass.states.set(self.entity_id, "on" if self._dev.state else "off", state.attributes)
    
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
        self._dev.turnOn()

    def turn_off(self, **kwargs):
        self._dev.turnOff()

    def update(self):
        """Fetch new state data for this light.
        This is the only method that should fetch new data for Home Assistant.
        """
        try:
            self._state = self._dev.state;
        except:
            pass
            
