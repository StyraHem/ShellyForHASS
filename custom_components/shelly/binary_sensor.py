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
try:
    from homeassistant.components.binary_sensor import BinarySensorEntity
except:
    from homeassistant.components.binary_sensor import \
        BinarySensorDevice as BinarySensorEntity
from homeassistant.helpers.restore_state import RestoreStateData

from . import (CONF_OBJECT_ID_PREFIX)
from .device import ShellyDevice
from .block import ShellyBlock

from .const import *

_LOGGER = logging.getLogger(__name__)

CLICK_EVENTS = {
    'S' : 'single',
    'SS' : 'double',
    'SSS': 'triple',
    'L': 'long',
    'SL': 'short-long',
    'LS': 'long-short'
}

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
                ShellyBinarySensor(dev, instance, dev.sensor_type,
                                   dev.sensor_type)
            ])

    async_dispatcher_connect(
        hass,
        "shelly_new_binary_sensor",
        async_discover_sensor
    )

class ShellySwitch(ShellyDevice, BinarySensorEntity):
    """Representation of a Shelly Switch state."""

    def __init__(self, dev, instance):
        """Initialize an ShellySwitch."""
        ShellyDevice.__init__(self, dev, instance)
        self._unique_id += "_switch"
        self.entity_id += "_switch"
        self._state = None
        self._click_delay = 700
        self._last_state_change = 0
        self._click_cnt = 0
        self._click_timer = None
        self._name_ext = "Switch"
        self._last_event = None
        self._event_cnt = None
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

    def _send_event(self, type):
        self.hass.bus.fire('shellyforhass.click', \
                            {'entity_id' : self.entity_id,
                             'click_type' : type})

    def update(self):
        """Fetch new state data for this switch."""
        millis = self._millis()
        new_state = None if self._dev.state is None else self._dev.state != 0
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
        if self._dev.event_cnt != self._event_cnt:
            event = CLICK_EVENTS.get(self._dev.last_event, None)
            if not self._event_cnt is None:
                self._send_event(event)
            self._event_cnt = self._dev.event_cnt
            self._last_event = event

    @property
    def device_state_attributes(self):
        attrs = super().device_state_attributes
        if self._last_event:
            attrs[ATTRIBUTE_CLICK_TYPE] = self._last_event
            attrs[ATTRIBUTE_CLICK_CNT] = self._event_cnt
        return attrs

class ShellyBinarySensor(ShellyDevice, BinarySensorEntity):
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
        self._master_unit = True
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

class ShellyBinaryInfoSensor(ShellyBlock, BinarySensorEntity):
    """Representation of a Shelly Info Sensor."""

    def __init__(self, block, instance, sensor_type, sensor_name):
        self._sensor_cfg = SENSOR_TYPES_CFG[SENSOR_TYPE_DEFAULT]
        ShellyBlock.__init__(self, block, instance, "_" + sensor_name)
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
