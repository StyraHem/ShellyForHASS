"""
Shelly platform for the sensor component.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""

import logging

from homeassistant.const import (
    DEVICE_CLASS_HUMIDITY, DEVICE_CLASS_TEMPERATURE, TEMP_CELSIUS, POWER_WATT)
from homeassistant.helpers.entity import Entity

from . import CONF_OBJECT_ID_PREFIX, SHELLY_CONFIG, ShellyDevice, get_device_from_hass

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPE_TEMPERATURE = 'temp'
SENSOR_TYPE_HUMIDITY = 'humidity'
SENSOR_TYPE_POWER = 'watt'
SENSOR_TYPE_RSSI = 'rssi'
SENSOR_TYPE_UPTIME = 'uptime'

SENSOR_TYPES = {
    SENSOR_TYPE_TEMPERATURE:
        ['Temperature', TEMP_CELSIUS, None, DEVICE_CLASS_TEMPERATURE],
    SENSOR_TYPE_HUMIDITY:
        ['Humidity', '%', None, DEVICE_CLASS_HUMIDITY],
    SENSOR_TYPE_POWER:
        ['Power', POWER_WATT, None, None],
    SENSOR_TYPE_RSSI:
        ['RSSI', 'dB', 'mdi:wifi', None],
    SENSOR_TYPE_UPTIME:
        ['Uptime', 's', 'mdi:timer', None]
}

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Shelly Sensor platform."""
    if 'version' in discovery_info:
        add_devices([ShellyVersion(hass, discovery_info.get('version'),
                                   discovery_info.get('pyShellyVersion'))])
        return

    dev = get_device_from_hass(hass, discovery_info)

    if 'rssi' in discovery_info:
        add_devices([
            ShellyInfoSensor(dev, hass, SENSOR_TYPE_RSSI, 'rssi')
        ])
        return

    if 'uptime' in discovery_info:
        add_devices([
            ShellyInfoSensor(dev, hass, SENSOR_TYPE_UPTIME, 'uptime')
        ])
        return

    if dev.device_type == "POWERMETER":
        add_devices([
            ShellySensor(dev, hass, SENSOR_TYPE_POWER, 'watt'),
        ])
    elif dev.device_type == "SENSOR":
        add_devices([
            ShellySensor(dev, hass, SENSOR_TYPE_TEMPERATURE, 'temperature'),
            ShellySensor(dev, hass, SENSOR_TYPE_HUMIDITY, 'humidity')
        ])


class ShellySensor(ShellyDevice, Entity):
    """Representation of a Shelly Sensor."""

    def __init__(self, dev, hass, sensor_type, sensor_name):
        """Initialize an ShellySwitch."""
        ShellyDevice.__init__(self, dev, hass)
        self._unique_id += "_" + sensor_name
        self.entity_id += "_" + sensor_name
        self._sensor_type = sensor_type
        self._sensor_name = sensor_name
        self._battery = None

        self._state = None
        self.update()

    def _updated(self):
        """Receive events when the switch state changed (by mobile,
        switch etc)"""
        self.schedule_update_ha_state(True)
        
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def quantity_name(self):
        """Name of quantity."""
        return SENSOR_TYPES[self._sensor_type][0] \
            if self._sensor_type in SENSOR_TYPES else None

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return SENSOR_TYPES[self._sensor_type][1] \
            if self._sensor_type in SENSOR_TYPES else None

    @property
    def icon(self):
        """Return the icon."""
        return SENSOR_TYPES[self._sensor_type][2] \
            if self._sensor_type in SENSOR_TYPES else None

    @property
    def device_class(self):
        """Return the device class."""
        return SENSOR_TYPES[self._sensor_type][3] \
            if self._sensor_type in SENSOR_TYPES else None

    def update(self):
        """Fetch new state data for this sensor."""
        try:
            self._state = self._dev.sensorValues[self._sensor_name]
            self._battery = self._dev.sensorValues.get('battery', None)
        except:
            pass

    @property
    def device_state_attributes(self):
        attr = super(ShellySensor, self).device_state_attributes
        if self._battery is not None:
            attr["battery"] = str(self._battery) + '%'
        return attr


class ShellyInfoSensor(ShellySensor, Entity):
    """Representation of a Shelly Info Sensor."""

    def __init__(self, dev, hass, sensor_type, sensor_name):
        ShellySensor.__init__(self, dev, hass, sensor_type, sensor_name)

    def _updated(self):
        """Receive events when the switch state changed (by mobile,
        switch etc)"""
        if self.entity_id is not None:
            state = self._hass.states.get(self.entity_id)
            if state is not None:
                self._state = self._dev.info_values[self._sensor_name]
                self._hass.states.set(self.entity_id, self._state,
                                      state.attributes)

    def update(self):
        """Fetch new state data for this sensor."""
        try:
            self._state = self._dev.info_values[self._sensor_name]
            self._battery = self._dev.sensorValues.get('battery', None)
        except:
            pass

    @property
    def device_state_attributes(self):
        return None


class ShellyVersion(Entity):
    """Representation of a Shelly version sensor."""

    def __init__(self, hass, version, py_shelly_version):
        """Initialize the Version sensor."""
        conf = hass.data[SHELLY_CONFIG]
        id_prefix = conf.get(CONF_OBJECT_ID_PREFIX)
        self._version = version
        self._py_shelly_version = py_shelly_version
        self.entity_id = "sensor." + id_prefix + "_version"
        self._name = "Shelly version"

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Shelly version'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._version + "/" + self._py_shelly_version

    @property
    def device_state_attributes(self):
        """Return attributes for the sensor."""
        return {'shelly': self._version, 'pyShelly': self._py_shelly_version}

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return None
