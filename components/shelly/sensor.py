"""
Shelly platform for the sensor component.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""

import logging
from . import (ShellyDevice, SHELLY_CONFIG, CONF_OBJECT_ID_PREFIX)
from homeassistant.const import (TEMP_CELSIUS, DEVICE_CLASS_TEMPERATURE, DEVICE_CLASS_HUMIDITY)
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
#PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
#})

SENSOR_TYPE_TEMPERATURE = 'temp'
SENSOR_TYPE_HUMIDITY = 'humidity'
SENSOR_TYPE_POWER = 'watt'

SENSOR_TYPES = {
    SENSOR_TYPE_TEMPERATURE:
        ['Temperature', TEMP_CELSIUS, None, DEVICE_CLASS_TEMPERATURE],
    SENSOR_TYPE_HUMIDITY:
        ['Humidity', '%', None, DEVICE_CLASS_HUMIDITY],
    SENSOR_TYPE_POWER:
        ['Power', 'W', None, None]
}

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Shelly Sensor platform."""
    if 'version' in discovery_info:
        add_devices([ ShellyVersion(hass, discovery_info.get('version'), 
                                    discovery_info.get('pyShellyVersion') ) ])   
        return
    dataKey = discovery_info['dataKey']
    dev = hass.data[dataKey]
    if dev.devType=="POWERMETER":
      add_devices([
        ShellySensor(dev, hass, SENSOR_TYPE_POWER, 'watt'),
      ])
    elif dev.devType=="SENSOR":
      add_devices([
        ShellySensor(dev, hass, SENSOR_TYPE_TEMPERATURE, 'temperature'),
        ShellySensor(dev, hass, SENSOR_TYPE_HUMIDITY, 'humidity')
      ])
    hass.data[dataKey]=None


class ShellySensor(ShellyDevice, Entity):
    """Representation of an Shelly Switch."""

    def __init__(self, dev, hass, type, sensorName):
        """Initialize an ShellySwitch."""
        ShellyDevice.__init__(self, dev, hass)
        self._unique_id += "_" + sensorName
        self.entity_id += "_" + sensorName
        self._type = type
        self._sensorName = sensorName
        self._battery = None
        
        self._state = None
        self.update()

    def _updated(self):
        """Receive events when the switch state changed (by mobile, switch etc)"""
        if self.entity_id is not None:
            state = self._hass.states.get(self.entity_id)
            if state is not None:
                self._state = self._dev.sensorValues[self._sensorName]
                self._hass.states.set(self.entity_id, self._state, state.attributes)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def quantity_name(self):
        """Name of quantity."""
        return SENSOR_TYPES[self._type][0] \
            if self._type in SENSOR_TYPES else None

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return SENSOR_TYPES[self._type][1] \
            if self._type in SENSOR_TYPES else None

    @property
    def icon(self):
        """Return the icon."""
        return SENSOR_TYPES[self._type][2] \
            if self._type in SENSOR_TYPES else None

    @property
    def device_class(self):
        """Return the device class."""
        return SENSOR_TYPES[self._type][3] \
            if self._type in SENSOR_TYPES else None
        
    def update(self):
        """Fetch new state data for this light.
        This is the only method that should fetch new data for Home Assistant.
        """
        try:
            self._state = self._dev.sensorValues[self._sensorName]
            self._battery = self._dev.sensorValues.get('battery',None)
        except:
            pass
            
    @property
    def device_state_attributes(self):
        attr = super(ShellySensor, self).device_state_attributes
        if self._battery is not None:
            attr["battery"] = str(self._battery) + '%'
        return attr

    
class ShellyVersion(Entity):
    """Representation of a Home Assistant version sensor."""

    def __init__(self, hass, version, pyShellyVersion):
        """Initialize the Version sensor."""
        conf = hass.data[SHELLY_CONFIG]
        idPrefix = conf.get(CONF_OBJECT_ID_PREFIX)
        self._version = version
        self._pyShellyVersion = pyShellyVersion
        self.entity_id = "sensor." + idPrefix + "_version"        
        self._name = "Shelly version"

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Shelly version'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._version + "/" + self._pyShellyVersion

    @property
    def device_state_attributes(self):
        """Return attributes for the sensor."""
        return {'shelly': self._version, 'pyShelly' : self._pyShellyVersion }

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return None