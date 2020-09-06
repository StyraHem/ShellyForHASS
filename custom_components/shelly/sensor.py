"""
Shelly platform for the sensor component.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""

import logging
import time
from threading import Timer
from homeassistant.util import slugify
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from homeassistant.const import (DEVICE_CLASS_HUMIDITY,
                                 DEVICE_CLASS_BATTERY,
                                 DEVICE_CLASS_ILLUMINANCE,
                                 DEVICE_CLASS_TEMPERATURE,
                                 TEMP_CELSIUS, POWER_WATT,
                                 STATE_ON, STATE_OFF)
from homeassistant.helpers.entity import Entity
from homeassistant.core import callback

from . import (CONF_OBJECT_ID_PREFIX)
from .device import ShellyDevice
from .block import ShellyBlock

from .const import *

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Shelly sensor dynamically."""
    async def async_discover_sensor(dev, instance):
        """Discover and add a discovered sensor."""
        if isinstance(dev, dict):
            if 'version' in dev:
                async_add_entities([ShellyVersion(
                    instance, dev.get('version'), dev.get('pyShellyVersion'),
                    dev.get('extra'))])
            if 'sensor_type' in dev:
                sensor_type = dev['sensor_type']
                async_add_entities([ShellyInfoSensor(dev['itm'], instance,
                                           sensor_type, sensor_type)])
            return
        if dev.device_type == "POWERMETER":
            async_add_entities([ShellySensor(dev, instance, SENSOR_TYPE_POWER,
                                'current_consumption', False),
            ])
        elif dev.device_type == "SENSOR":
            async_add_entities([
                ShellySensor(dev, instance, dev.sensor_type, dev.sensor_type,
                             True)
            ])

    async_dispatcher_connect(
        hass,
        "shelly_new_sensor",
        async_discover_sensor
    )

class ShellySensor(ShellyDevice):
    """Representation of a Shelly Sensor."""

    def __init__(self, dev, instance, sensor_type, sensor_name, master_unit):
        """Initialize an ShellySensor."""
        self._sensor_cfg = SENSOR_TYPES_CFG[SENSOR_TYPE_DEFAULT]
        ShellyDevice.__init__(self, dev, instance)
        self._unique_id += "_" + sensor_name
        self.entity_id += "_" + sensor_name
        self._sensor_type = sensor_type
        self._sensor_name = sensor_name
        self._battery = None
        self._config = instance.conf
        self._state = None
        if self._sensor_type in SENSOR_TYPES_CFG:
            self._sensor_cfg = SENSOR_TYPES_CFG[self._sensor_type]
        #settings = instance._get_setting(sensor_type, dev.id, dev.block.id)
        self._sensor_settings = self._settings.get(sensor_type, {})
        self._unit = self._sensor_settings.get(CONF_UNIT)
        self._master_unit = master_unit
        self.update()

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._sensor_cfg[4] == "bool":
            return STATE_ON if self._state else STATE_OFF
        return self._state

    @property
    def quantity_name(self):
        """Name of quantity."""
        return self._sensor_cfg[0]

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit or self._sensor_cfg[1]

    @property
    def icon(self):
        """Return the icon."""
        return self._sensor_cfg[2]

    @property
    def device_class(self):
        """Return the device class."""
        return self._sensor_cfg[3]

    def update(self):
        """Fetch new state data for this sensor."""
        #if self._dev.sensor_values is not None:
        state = self._dev.state #sensor_values.get(self._sensor_name, None)
        if state is not None:
            state = self.instance.format_value(self._sensor_settings, state)
        self._state = state

        if self._dev.info_values is not None:
            self._battery = self._dev.info_values.get('battery', None)

class ShellyInfoSensor(ShellyBlock):
    """Representation of a Shelly Info Sensor."""

    def __init__(self, block, instance, sensor_type, sensor_name):
        self._sensor_cfg = SENSOR_TYPES_CFG[SENSOR_TYPE_DEFAULT]
        ShellyBlock.__init__(self, block, instance, "_" + sensor_name)
        self.entity_id = "sensor" + self.entity_id
        self._sensor_name = sensor_name
        self._sensor_type = sensor_type
        if self._sensor_type in SENSOR_TYPES_CFG:
            self._sensor_cfg = SENSOR_TYPES_CFG[self._sensor_type]
        #settings = instance._get_setting(sensor_type, block.id, None)
        self._sensor_settings = self._settings.get(sensor_type, {})
        self._unit = self._sensor_settings.get(CONF_UNIT)
        self._state = None
        self._name_ext = self.quantity_name()
        self.update()

    def update(self):
        """Fetch new state data for this sensor."""
        if self._block.info_values is not None:
            state = self._block.info_values.get(self._sensor_name, None)
            state = self.instance.format_value(self._sensor_settings, state)
            self._state = state

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def quantity_name(self):
        """Name of quantity."""
        return self._sensor_cfg[0]

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit or self._sensor_cfg[1]

    @property
    def icon(self):
        """Return the icon."""
        return self._sensor_cfg[2]

    @property
    def device_class(self):
        """Return the device class."""
        return self._sensor_cfg[3]

class ShellyVersion(Entity):
    """Representation of a Shelly version sensor."""

    def __init__(self, instance, version, py_shelly_version, extra):
        """Initialize the Version sensor."""
        conf = instance.conf
        id_prefix = slugify(conf.get(CONF_OBJECT_ID_PREFIX))
        self._version = version
        self._py_shelly_version = py_shelly_version
        self.entity_id = "sensor." + id_prefix + "_version"
        self._name = "ShellyForHass"
        self._extra = extra
        #self.instance = instance

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._version #+ "/" + self._py_shelly_version

    @property
    def device_state_attributes(self):
        """Return attributes for the sensor."""
        attribs = {'shelly': self._version,
                'pyShelly': self._py_shelly_version,
                'developed_by': "StyraHem.se"}
        if self._extra:
            attribs.update(self._extra)
        return attribs

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return None

    @property
    def unique_id(self):
        """Return the ID of this device."""
        return 'sensor.version'

    @property
    def device_info(self):
        return {
            'identifiers': {
                (DOMAIN, 'version')
            },
            'name': "ShellyForHASS",
            'manufacturer': 'StyraHem.se',
            'model': self._version,
            'sw_version': self._version
        }