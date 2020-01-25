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
from homeassistant.components.binary_sensor import BinarySensorDevice
from homeassistant.helpers.restore_state import RestoreStateData

from . import (CONF_OBJECT_ID_PREFIX, CONF_POWER_DECIMALS, SHELLY_CONFIG,
               ShellyDevice, ShellyBlock)

from .const import *

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Shelly sensor dynamically."""
    async def async_discover_sensor(dev, instance):
        """Discover and add a discovered sensor."""
        if isinstance(dev, dict):
            if 'sensor_type' in dev:
                sensor_type = dev['sensor_type']
                async_add_entities([ShellyBinaryInfoSensor(dev['itm'], instance,
                                           sensor_type, sensor_type)])
            return
        if dev.device_type == "SWITCH":
            async_add_entities([ShellySwitch(dev, instance)])
        elif dev.device_type == "BINARY_SENSOR":
            async_add_entities([
                ShellyBinarySensor(dev, instance, dev.sensor_type, dev.sensor_type)
            ])

    async_dispatcher_connect(
        hass,
        "shelly_new_binary_sensor",
        async_discover_sensor
    )

class ShellySwitch(ShellyDevice, BinarySensorDevice):
    """Representation of a Shelly Switch state."""

    def __init__(self, dev, instance):
        """Initialize an ShellySwitch."""
        ShellyDevice.__init__(self, dev, instance)
        self._unique_id += "_switch"
        self.entity_id += "_switch"
        self._state = None
        self._click_delay = 500
        self._last_state_change = 0
        self._click_cnt = 0
        self._click_timer = None
        self._name_ext = "Switch"
        self.update()

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self._state

    @property
    def icon(self):
        """Return the button icon."""
        return "mdi:hockey-puck"

    def _millis(self):
        return int(round(time.time() * 1000))

    def _click_timeout(self):
        self._send_click_event()
        self._click_cnt = 0
        self._click_timer = None

    def _send_click_event(self):
        self.hass.bus.fire('shelly_switch_click', \
                            {'entity_id' : self.entity_id,
                             'click_cnt': self._click_cnt,
                             'state' : self._state})

    def update(self):
        """Fetch new state data for this switch."""
        millis = self._millis()
        new_state = self._dev.state != 0
        if self._state is not None and new_state != self._state:
            if self._click_timer is not None:
                self._click_timer.cancel()
            diff = millis - self._last_state_change
            if diff < self._click_delay or self._click_cnt == 0:
                self._click_cnt += 1
            else:
                self._click_cnt = 1
            self._last_state_change = millis
            self._click_timer = Timer(self._click_delay/1000,
                                        self._click_timeout)
            self._click_timer.start()
        self._state = new_state

class ShellyBinarySensor(ShellyDevice, BinarySensorDevice):
    """Representation of a Shelly Sensor."""

    def __init__(self, dev, instance, sensor_type, sensor_name):
        """Initialize an ShellySensor."""
        self._sensor_cfg = SENSOR_TYPES_CFG[SENSOR_TYPE_DEFAULT]
        ShellyDevice.__init__(self, dev, instance)
        self._unique_id += "_" + sensor_name
        self.entity_id += "_" + sensor_name
        self._sensor_type = sensor_type
        self._sensor_name = sensor_name
        #self._battery = None
        self._config = instance.conf
        self._state = None
        if self._sensor_type in SENSOR_TYPES_CFG:
            self._sensor_cfg = SENSOR_TYPES_CFG[self._sensor_type]
        self.update()

    @property
    def is_on(self):
        """State"""
        return self._state

    @property
    def quantity_name(self):
        """Name of quantity."""
        return self._sensor_cfg[0]

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._sensor_cfg[1]

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
        self._state = self._dev.state

class ShellyBinaryInfoSensor(ShellyBlock, BinarySensorDevice):
    """Representation of a Shelly Info Sensor."""

    def __init__(self, block, instance, sensor_type, sensor_name):
        self._sensor_cfg = SENSOR_TYPES_CFG[SENSOR_TYPE_DEFAULT]
        ShellyBlock.__init__(self, block, instance, "_" + sensor_name + "_attr")
        self.entity_id = "sensor" + self.entity_id
        self._sensor_name = sensor_name
        self._sensor_type = sensor_type
        if self._sensor_type in SENSOR_TYPES_CFG:
            self._sensor_cfg = SENSOR_TYPES_CFG[self._sensor_type]
        self._state = None
        self._name_ext = self.quantity_name()
        self.update()

    def update(self):
        """Fetch new state data for this sensor."""
        if self._block.info_values is not None:
            self._state = self._block.info_values.get(self._sensor_name, None)

    @property
    def is_on(self):
        """Return the state of the sensor."""
        return self._state

    def quantity_name(self):
        """Name of quantity."""
        return self._sensor_cfg[0]

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._sensor_cfg[1]

    @property
    def icon(self):
        """Return the icon."""
        return self._sensor_cfg[2]

    @property
    def device_class(self):
        """Return the device class."""
        return self._sensor_cfg[3]
