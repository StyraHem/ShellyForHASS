"""
Shelly platform for the sensor component.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""

import logging
import time
from threading import Timer
from homeassistant.util import slugify

from homeassistant.const import (DEVICE_CLASS_HUMIDITY,
                                 DEVICE_CLASS_TEMPERATURE,
                                 TEMP_CELSIUS, POWER_WATT,
                                 STATE_ON, STATE_OFF)
from homeassistant.helpers.entity import Entity

from . import (CONF_OBJECT_ID_PREFIX, CONF_POWER_DECIMALS, SHELLY_CONFIG,
               ShellyDevice, get_device_from_hass,
               ShellyBlock, get_block_from_hass)

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPE_TEMPERATURE = 'temperature'
SENSOR_TYPE_HUMIDITY = 'humidity'
SENSOR_TYPE_POWER = 'consumption'
SENSOR_TYPE_RSSI = 'rssi'
SENSOR_TYPE_UPTIME = 'uptime'
SENSOR_TYPE_BATTERY = 'battery'
SENSOR_TYPE_OVER_POWER = 'over_power'
SENSOR_TYPE_DEVICE_TEMP = 'device_temp'
SENSOR_TYPE_OVER_TEMP = 'over_temp'
SENSOR_TYPE_CLOUD_STATUS = 'cloud_status'
SENSOR_TYPE_MQTT_CONNECTED = 'mqtt_connected'
SENSOR_TYPE_SWITCH = 'switch'
SENSOR_TYPE_FLOOD = 'flood'
SENSOR_TYPE_DEFAULT = 'default'

SENSOR_TYPES_CFG = {
    SENSOR_TYPE_DEFAULT:
        [None, None, None, None, None],
    SENSOR_TYPE_TEMPERATURE:
        ['Temperature', TEMP_CELSIUS, None, DEVICE_CLASS_TEMPERATURE, None],
    SENSOR_TYPE_HUMIDITY:
        ['Humidity', '%', None, DEVICE_CLASS_HUMIDITY, None],
    SENSOR_TYPE_POWER:
        ['Consumption', POWER_WATT, None, None, None],
    SENSOR_TYPE_RSSI:
        ['RSSI', 'dB', 'mdi:wifi', None, None],
    SENSOR_TYPE_UPTIME:
        ['Uptime', 's', 'mdi:timer', None, None],
    SENSOR_TYPE_BATTERY:
        ['Battery', '%', 'mdi:battery-50', None, None],
    SENSOR_TYPE_OVER_POWER:
        ['Over power', '', 'mdi:alert', None, None],
    SENSOR_TYPE_DEVICE_TEMP:
        ['Device temperature', TEMP_CELSIUS, "mdi:oil-temperature", None, None],
    SENSOR_TYPE_OVER_TEMP:
        ['Over temperature', '', 'mdi:alert', None, None],
    SENSOR_TYPE_CLOUD_STATUS:
        ['Cloud status', '', 'mdi:transit-connection-variant', None, None],
    SENSOR_TYPE_MQTT_CONNECTED:
        ['MQTT connected', '', 'mdi:transit-connection-variant', None, None],  
    SENSOR_TYPE_FLOOD:
        ['Flood', '', 'mdi:water', None, 'bool']
}

def setup_platform(hass, _config, add_devices, discovery_info=None):
    """Setup the Shelly Sensor platform."""
    if 'version' in discovery_info:
        add_devices([ShellyVersion(hass, discovery_info.get('version'),
                                   discovery_info.get('pyShellyVersion'))])
        return

    if 'sensor_type' in discovery_info:        
        sensor_type = discovery_info['sensor_type']
        block = get_block_from_hass(hass, discovery_info)
        if block is not None:
            add_devices([ShellyInfoSensor(block, hass, sensor_type, sensor_type)])
        else:
            dev = get_device_from_hass(hass, discovery_info)
            add_devices([ShellyInfoSensor(dev, hass, sensor_type, sensor_type)])
        return

    dev = get_device_from_hass(hass, discovery_info)

    if dev.device_type == "POWERMETER":
        add_devices([
            ShellySensor(dev, hass, SENSOR_TYPE_POWER, 'consumption'),
        ])
    elif dev.device_type == "SENSOR":
        add_devices([ShellySensor(dev, hass, dev.sensor_type, dev.sensor_type)])
    elif dev.device_type == "SWITCH":
        add_devices([ ShellySwitch(dev, hass) ])

class ShellySensor(ShellyDevice, Entity):
    """Representation of a Shelly Sensor."""

    def __init__(self, dev, hass, sensor_type, sensor_name):
        """Initialize an ShellySensor."""
        self._sensor_cfg = SENSOR_TYPES_CFG[SENSOR_TYPE_DEFAULT]
        ShellyDevice.__init__(self, dev, hass)
        self._unique_id += "_" + sensor_name
        self.entity_id += "_" + sensor_name
        self._sensor_type = sensor_type
        self._sensor_name = sensor_name
        self._battery = None
        self._config = hass.data[SHELLY_CONFIG]
        self._state = None
        if self._sensor_type in SENSOR_TYPES_CFG:
            self._sensor_cfg = SENSOR_TYPES_CFG[self._sensor_type]
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
        if self._dev.sensor_values is not None:
            self._state = self._dev.sensor_values.get(self._sensor_name, None)
            power_decimals = self._config.get(CONF_POWER_DECIMALS, None)
            if self._state is not None \
                and self._sensor_type == SENSOR_TYPE_POWER \
                and power_decimals is not None:
                if power_decimals > 0:
                    self._state = round(self._state, power_decimals)
                elif power_decimals == 0:
                    self._state = round(self._state)
            self._battery = self._dev.sensor_values.get('battery', None)


class ShellySwitch(ShellyDevice, Entity):
    """Representation of a Shelly Swwitch state."""

    def __init__(self, dev, hass):
        """Initialize an ShellySwitch."""
        ShellyDevice.__init__(self, dev, hass)
        self._unique_id += "_switch"
        self.entity_id += "_switch"
        self._state = None
        self._click_delay = 500
        self._last_state_change = 0
        self._click_cnt = 0
        self._click_timer = None
        self.update()

    @property
    def state(self):
        """Return the state of the switch."""
        return STATE_ON if self._state else STATE_OFF

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
                             'state' : self._state })

    def update(self):
        """Fetch new state data for this switch."""        
        if self._dev.sensor_values is not None:
            ms = self._millis()
            new_state = self._dev.sensor_values.get("switch", None) != 0
            if self._state is not None and new_state != self._state:                
                if self._click_timer is not None:
                    self._click_timer.cancel()
                diff = ms - self._last_state_change 
                if diff < self._click_delay or self._click_cnt == 0:
                    self._click_cnt += 1
                else:
                    self._click_cnt = 1
                self._last_state_change = ms                
                self._click_timer = Timer(self._click_delay/1000, self._click_timeout)
                self._click_timer.start()
            self._state = new_state
                
class ShellyInfoSensor(ShellyBlock, Entity):
    """Representation of a Shelly Info Sensor."""

    def __init__(self, block, hass, sensor_type, sensor_name):
        self._sensor_cfg = SENSOR_TYPES_CFG[SENSOR_TYPE_DEFAULT]
        ShellyBlock.__init__(self, block, hass, "_" + sensor_name + "_attr")
        self.entity_id = "sensor" + self.entity_id
        self._sensor_name = sensor_name
        self._sensor_type = sensor_type
        if self._sensor_type in SENSOR_TYPES_CFG:
            self._sensor_cfg = SENSOR_TYPES_CFG[self._sensor_type]
        self._state = None
        self._name += " - " + self.quantity_name()
        self.update()

    def update(self):
        """Fetch new state data for this sensor."""
        if self._block.info_values is not None:
            self._state = self._block.info_values.get(self._sensor_name, None)

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
        return self._sensor_cfg[1]

    @property
    def icon(self):
        """Return the icon."""
        return self._sensor_cfg[2]

    #@property
    #def device_state_attributes(self):
    #    return None


class ShellyVersion(Entity):
    """Representation of a Shelly version sensor."""

    def __init__(self, hass, version, py_shelly_version):
        """Initialize the Version sensor."""
        conf = hass.data[SHELLY_CONFIG]
        id_prefix = slugify(conf.get(CONF_OBJECT_ID_PREFIX))
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
