"""
Shelly platform for the sensor component.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""

import logging

from homeassistant.const import (DEVICE_CLASS_HUMIDITY,
                                 DEVICE_CLASS_TEMPERATURE,
                                 TEMP_CELSIUS, POWER_WATT)
from homeassistant.helpers.entity import Entity

from . import (CONF_OBJECT_ID_PREFIX, CONF_POWER_DECIMALS, SHELLY_CONFIG,
               ShellyDevice, get_device_from_hass,
               ShellyBlock, get_block_from_hass)

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPE_TEMPERATURE = 'temp'
SENSOR_TYPE_HUMIDITY = 'humidity'
SENSOR_TYPE_POWER = 'watt'
SENSOR_TYPE_RSSI = 'rssi'
SENSOR_TYPE_UPTIME = 'uptime'
SENSOR_TYPE_BATTERY = 'battery'

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
        ['Uptime', 's', 'mdi:timer', None],
    SENSOR_TYPE_BATTERY:
        ['Battery', '%', 'mdi:battery-50', None]
}

def setup_platform(hass, _config, add_devices, discovery_info=None):
    """Setup the Shelly Sensor platform."""
    if 'version' in discovery_info:
        add_devices([ShellyVersion(hass, discovery_info.get('version'),
                                   discovery_info.get('pyShellyVersion'))])
        return

    if 'rssi' in discovery_info:
        block = get_block_from_hass(hass, discovery_info)
        add_devices([
            ShellyInfoSensor(block, hass, SENSOR_TYPE_RSSI, 'rssi')
        ])
        return

    if 'uptime' in discovery_info:
        block = get_block_from_hass(hass, discovery_info)
        add_devices([
            ShellyInfoSensor(block, hass, SENSOR_TYPE_UPTIME, 'uptime')
        ])
        return

    dev = get_device_from_hass(hass, discovery_info)

    if dev.device_type == "POWERMETER":
        add_devices([
            ShellySensor(dev, hass, SENSOR_TYPE_POWER, 'watt'),
        ])
    elif dev.device_type == "SENSOR":
        add_devices([
            ShellySensor(dev, hass, SENSOR_TYPE_TEMPERATURE, 'temperature'),
            ShellySensor(dev, hass, SENSOR_TYPE_HUMIDITY, 'humidity'),
            ShellySensor(dev, hass, SENSOR_TYPE_BATTERY, 'battery')
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
        self._config = hass.data[SHELLY_CONFIG]

        self._state = None
        self.update()

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
        if self._dev.sensor_values is not None:
            self._state = self._dev.sensor_values.get(self._sensor_name, None)
            power_decimals = self._config.get(CONF_POWER_DECIMALS, None)
            if self._state is not None and self._sensor_type == SENSOR_TYPE_POWER and power_decimals is not None:
                if power_decimals > 0:
                    self._state = round(self._state, power_decimals)
                elif power_decimals == 0:
                    self._state = round(self._state)

            self._battery = self._dev.sensor_values.get('battery', None)

    @property
    def device_state_attributes(self):
        attr = super(ShellySensor, self).device_state_attributes
        if self._battery is not None:
            attr["battery"] = str(self._battery) + '%'
        return attr


class ShellyInfoSensor(ShellyBlock, Entity):
    """Representation of a Shelly Info Sensor."""

    def __init__(self, block, hass, sensor_type, sensor_name):
        ShellyBlock.__init__(self, block, hass, "_" + sensor_name)
        self.entity_id = "sensor" + self.entity_id
        self._sensor_name = sensor_name
        self._sensor_type = sensor_type
        self._state = None
        self.update()

    def update(self):
        """Fetch new state data for this sensor."""
        if self._block.info_values is not None:
            self._state = self._block.info_values.get(self._sensor_name, None)
        #if self._block.sensor_values is not None:
        #    self._battery = self._block.sensor_values.get('battery', None)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state
        
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
