"""
Support for Shelly smart home devices.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/shelly/
"""
from datetime import timedelta
import logging

import voluptuous as vol

from homeassistant.const import (
    CONF_DEVICES, CONF_DISCOVERY, CONF_ID, CONF_NAME, CONF_PASSWORD,
    CONF_SCAN_INTERVAL, CONF_USERNAME, EVENT_HOMEASSISTANT_STOP)
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.script import Script
from homeassistant.util import slugify

import time

REQUIREMENTS = ['pyShelly==0.1.0']

_LOGGER = logging.getLogger(__name__)

__version__ = "0.1.0"
VERSION = __version__

DOMAIN = 'shelly'

CONF_ADDITIONAL_INFO = 'additional_information'
CONF_IGMPFIX = 'igmp_fix'
CONF_LIGHT_SWITCH = 'light_switch'
CONF_OBJECT_ID_PREFIX = 'id_prefix'
CONF_ENTITY_ID = 'entity_id'
CONF_SHOW_ID_IN_NAME = 'show_id_in_name'
CONF_VERSION = 'version'
CONF_POWER_DECIMALS = 'power_decimals'
CONF_SENSORS = 'sensors'
CONF_UPGRADE_SWITCH = 'upgrade_switch'
CONF_UNAVALABLE_AFTER_SEC = 'unavailable_after_sec'
CONF_LOCAL_PY_SHELLY = 'debug_local_py_shelly'
CONF_ONLY_DEVICE_ID = 'debug_only_device_id'

CONF_WIFI_SENSOR = 'wifi_sensor' #deprecated
CONF_UPTIME_SENSOR = 'uptime_sensor' #deprecated

DEFAULT_IGMPFIX = False
DEFAULT_DISCOVERY = True
DEFAULT_OBJECT_ID_PREFIX = 'shelly'
DEFAULT_SCAN_INTERVAL = timedelta(seconds=60)
DEFAULT_SHOW_ID_IN_NAME = True

SHELLY_DEVICES = 'shelly_devices'
SHELLY_BLOCKS = 'shelly_blocks'
SHELLY_CONFIG = 'shelly_cfg'
SHELLY_DEVICE_ID = 'device_id'
SHELLY_BLOCK_ID = 'block_id'

SENSOR_ALL = 'all'
SENSOR_RSSI = 'rssi'
SENSOR_POWER = 'power'
SENSOR_UPTIME = 'uptime'
SENSOR_OVER_POWER = 'over_power'
SENSOR_DEV_TEMP = 'device_temp'
SENSOR_OVER_TEMP = 'over_temp'
SENSOR_CLOUD = 'cloud'
SENSOR_MQTT = 'mqtt'
SENSOR_BATTERY = 'battery'
SENSOR_SWITCH = 'switch'

SENSOR_TYPES = {
    SENSOR_ALL: {},
    SENSOR_RSSI: {'attr':'rssi'},
    SENSOR_UPTIME: {'attr':'uptime'},
    SENSOR_POWER: {},
    SENSOR_OVER_POWER: {'attr':'over_power'},
    SENSOR_DEV_TEMP: {'attr':'device_temp'},
    SENSOR_OVER_TEMP: {'attr':'over_temp'},
    SENSOR_CLOUD:  {'attr':'cloud_status'},
    SENSOR_MQTT:  {'attr':'mqtt_connected'},
    SENSOR_BATTERY : {'attr':'battery'},
    SENSOR_SWITCH : {}
}

SENSOR_SCHEMA = vol.Schema({
    vol.Optional(CONF_NAME): cv.string,
})

DEVICE_SCHEMA = vol.Schema({
    vol.Required(CONF_ID): cv.string,
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_LIGHT_SWITCH, default=False): cv.boolean,
    vol.Optional(CONF_SENSORS):
            vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
    vol.Optional(CONF_UPGRADE_SWITCH): cv.boolean,
    vol.Optional(CONF_UNAVALABLE_AFTER_SEC) : cv.positive_int,
    vol.Optional(CONF_ENTITY_ID): cv.string,
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_IGMPFIX,
                     default=DEFAULT_IGMPFIX): cv.boolean,
        vol.Optional(CONF_SHOW_ID_IN_NAME,
                     default=DEFAULT_SHOW_ID_IN_NAME): cv.boolean,
        vol.Optional(CONF_DISCOVERY,
                     default=DEFAULT_DISCOVERY): cv.boolean,
        vol.Optional(CONF_OBJECT_ID_PREFIX,
                     default=DEFAULT_OBJECT_ID_PREFIX): cv.string,        
        vol.Optional(CONF_USERNAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_DEVICES,
                     default=[]): vol.All(cv.ensure_list, [DEVICE_SCHEMA]),
        vol.Optional(CONF_VERSION,
                     default=False): cv.boolean,
        vol.Optional(CONF_WIFI_SENSOR): cv.boolean, #deprecated
        vol.Optional(CONF_UPTIME_SENSOR): cv.boolean, #deprecated
        vol.Optional(CONF_UPGRADE_SWITCH,
                      default=True): cv.boolean,
        vol.Optional(CONF_UNAVALABLE_AFTER_SEC,
                    default=60) : cv.positive_int,
        vol.Optional(CONF_SENSORS,
                     default=[SENSOR_POWER]): vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES) ]),
        vol.Optional(CONF_ADDITIONAL_INFO,
                     default=True): cv.boolean,
        vol.Optional(CONF_SCAN_INTERVAL,
                     default=DEFAULT_SCAN_INTERVAL): cv.time_period,
        vol.Optional(CONF_POWER_DECIMALS): cv.positive_int,        
        vol.Optional(CONF_LOCAL_PY_SHELLY,
                     default=False): cv.boolean,
        vol.Optional(CONF_ONLY_DEVICE_ID) : cv.string
    })
}, extra=vol.ALLOW_EXTRA)

BLOCKS = {}
DEVICES = {}
BLOCK_SENSORS = []
DEVICE_SENSORS = []

def _get_block_key(block):
    key = block.id
    if not key in BLOCKS:
        BLOCKS[key] = block
    return key

def get_block_from_hass(hass, discovery_info):
    """Get block from HASS"""
    if SHELLY_BLOCK_ID in discovery_info:
        key = discovery_info[SHELLY_BLOCK_ID]
        return hass.data[SHELLY_BLOCKS][key] 

def _dev_key(dev):
    key = dev.id + "-" + dev.device_type   
    if dev.device_sub_type is not None:
        key += "-" + dev.device_sub_type
    return key

def _get_device_key(dev):
    key = _dev_key(dev)
    if not key in DEVICES:
        DEVICES[key] = dev
    return key

def get_device_from_hass(hass, discovery_info):
    """Get device from HASS"""
    device_key = discovery_info[SHELLY_DEVICE_ID]
    return hass.data[SHELLY_DEVICES][device_key]  

def _find_device_config(conf, id):
    device_conf_list = conf.get(CONF_DEVICES)
    for item in device_conf_list:
        if item[CONF_ID].upper() == id:
            return item
    return None

def _get_device_config(conf, id, id_2=None):
    """Get config for device."""
    item = _find_device_config(conf, id)
    if item is None and id_2 is not None:
        item = _find_device_config(conf, id_2)
    if item is None:
        return {}
    return item

def _get_specific_config(conf, key, default, *ids):
    for id in ids:
        item = _find_device_config(conf, id)
        if item is not None and key in item:
            return item[key]
    return default

def _get_specific_config_root(conf, key, *ids):
    item = _get_specific_config(conf, key, None, *ids)
    if item == None:
        item = conf.get(key)
    return item

def _get_sensor_config(conf, *ids):
    sensors = _get_specific_config(conf, CONF_SENSORS, None, *ids)
    if sensors is None:
        sensors = conf.get(CONF_SENSORS)
    if SENSOR_ALL in sensors:
        return [*SENSOR_TYPES.keys()]
    if sensors is None:
        return {}
    return sensors

def setup(hass, config):
    """Setup Shelly component"""
    _LOGGER.info("Starting shelly, %s", __version__)

    conf = config.get(DOMAIN, {})
    update_interval = conf.get(CONF_SCAN_INTERVAL)
    additional_info = conf.get(CONF_ADDITIONAL_INFO)
    hass.data[SHELLY_CONFIG] = conf
    discover = conf.get(CONF_DISCOVERY)

    if conf.get(CONF_LOCAL_PY_SHELLY):
        _LOGGER.info("Loading local pyShelly")
        from .pyShelly import pyShelly
    else:
        from pyShelly import pyShelly

    hass.data[SHELLY_DEVICES] = DEVICES
    hass.data[SHELLY_BLOCKS] = BLOCKS

    if conf.get(CONF_WIFI_SENSOR) is not None: 
        _LOGGER.warning("wifi_sensor is deprecated, use rssi in sensors instead.")
        if conf.get(CONF_WIFI_SENSOR) and SENSOR_RSSI not in conf[CONF_SENSORS]:
            conf[CONF_SENSORS].append(SENSOR_RSSI)
             
    if conf.get(CONF_UPTIME_SENSOR) is not None: 
        _LOGGER.warning("uptime_sensor is deprecated, use uptime in sensors instead.")
        if conf.get(CONF_UPTIME_SENSOR) and SENSOR_UPTIME not in conf[CONF_SENSORS]:
            conf[CONF_SENSORS].append(SENSOR_UPTIME)

    def _block_updated(block):
        
        hass_data = block.hass_data

        if hass_data['discover']:
            if hass_data['allow_upgrade_switch'] == True:
                has_update = block.info_values.get('has_firmware_update', False)
                update_switch = getattr(block, 'firmware_switch', None)
                if has_update:                        
                    if update_switch is None:
                        attr = {'firmware': True,
                                SHELLY_BLOCK_ID : _get_block_key(block)}
                        discovery.load_platform(hass, 'switch', DOMAIN, attr, conf)
                elif update_switch is not None:
                    update_switch.remove()

            block_key = _get_block_key(block)        
            for key, _value in block.info_values.items():
                ukey = block.id + '-' + key
                if not ukey in BLOCK_SENSORS:
                    BLOCK_SENSORS.append(ukey)                
                    for sensor in hass_data['sensor_cfg']:
                        if SENSOR_TYPES[sensor].get('attr') == key:
                            attr = {'sensor_type':key,
                                    SHELLY_BLOCK_ID : block_key}
                            discovery.load_platform(hass, 'sensor',
                                                    DOMAIN, attr, conf)

    def _block_added(block):
        block.cb_updated.append(_block_updated)
        _get_block_key(block)

        discover_block = discover or _get_device_config(conf, block.id) != {}

        block.hass_data = {
            'allow_upgrade_switch' : _get_specific_config_root(conf, CONF_UPGRADE_SWITCH, block.id),
            'sensor_cfg' : _get_sensor_config(conf, block.id),
            'discover': discover_block
        }
        
        #Config block
        if block.unavailable_after_sec is None:
            block.unavailable_after_sec \
                = _get_specific_config_root(conf, CONF_UNAVALABLE_AFTER_SEC,
                                                block.id)

        #if conf.get(CONF_ADDITIONAL_INFO):
            #block.update_status_information()
            # cfg_sensors = conf.get(CONF_SENSORS)
            # for sensor in cfg_sensors:                
            #     sensor_type = SENSOR_TYPES[sensor]                
            #     if 'attr' in sensor_type:
            #         attr = {'sensor_type':sensor_type['attr'],
            #                 SHELLY_BLOCK_ID : block_key}
            #         discovery.load_platform(hass, 'sensor', DOMAIN, attr, 
            #                                 config)

    def _device_added(dev, _code):
        device_key = _get_device_key(dev)
        attr = {SHELLY_DEVICE_ID : device_key}

        device_config = _get_device_config(conf, dev.id, dev.block.id)
        if not discover and device_config == {}:
            return

        if dev.device_type == "ROLLER":
            discovery.load_platform(hass, 'cover', DOMAIN, attr, config)
        elif dev.device_type == "RELAY":
            if device_config.get(CONF_LIGHT_SWITCH):
                discovery.load_platform(hass, 'light', DOMAIN, attr, config)
            else:
                discovery.load_platform(hass, 'switch', DOMAIN, attr, config)
        elif dev.device_type == 'POWERMETER':
            sensor_cfg = _get_sensor_config(conf, dev.id, dev.block.id)
            if SENSOR_POWER in sensor_cfg:
                discovery.load_platform(hass, 'sensor', DOMAIN, attr, config)
        elif dev.device_type == 'SWITCH':
            sensor_cfg = _get_sensor_config(conf, dev.id, dev.block.id)
            if SENSOR_SWITCH in sensor_cfg:
                discovery.load_platform(hass, 'sensor', DOMAIN, attr, config)
        elif dev.device_type in ["SENSOR"]: #, "INFOSENSOR"]:            
            discovery.load_platform(hass, 'sensor', DOMAIN, attr, config)
        elif dev.device_type in ["LIGHT", "DIMMER"]:
            discovery.load_platform(hass, 'light', DOMAIN, attr, config)

    def _device_removed(dev, _code):
        dev.shelly_device.remove()
        try:
            key = _dev_key(dev)
            del DEVICES[key]
        except KeyError:
            pass

    pys = pyShelly()
    _LOGGER.info("pyShelly, %s", pys.version())
    pys.cb_block_added.append(_block_added)
    pys.cb_device_added.append(_device_added)
    pys.cb_device_removed.append(_device_removed)
    pys.username = conf.get(CONF_USERNAME)
    pys.password = conf.get(CONF_PASSWORD)
    if additional_info:
        pys.update_status_interval = update_interval
    pys.only_device_id = conf.get(CONF_ONLY_DEVICE_ID)
    pys.igmp_fix_enabled = conf.get(CONF_IGMPFIX)
    pys.open()
    #pys.discover()

    if conf.get(CONF_VERSION):
        attr = {'version': VERSION, 'pyShellyVersion': pys.version()}
        discovery.load_platform(hass, 'sensor', DOMAIN, attr, config)

    def stop_shelly(_):
        """Stop Shelly."""
        _LOGGER.info("Shutting down Shelly")
        pys.close()

    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, stop_shelly)

    #def update_status_information():
    #    pys.update_status_information()
        #for _, block in pys.blocks.items():
        #    block.update_status_information()

    #async def update_domain_callback(_now):
    #    """Update the Shelly status information"""
    #    await hass.async_add_executor_job(update_status_information)

    #if conf.get(CONF_ADDITIONAL_INFO):
    #    hass.helpers.event.async_track_time_interval(
    #        update_domain_callback, update_interval)

    return True

class ShellyBlock(Entity):
    """Base class for Shelly entities"""

    def __init__(self, block, hass, prefix=""):
        conf = hass.data[SHELLY_CONFIG]
        id_prefix = conf.get(CONF_OBJECT_ID_PREFIX)        
        self._unique_id = slugify(id_prefix + "_" + block.type + "_" +
                                  block.id + prefix)
        self.entity_id = "." + self._unique_id
        entity_id = _get_specific_config(conf, CONF_ENTITY_ID , None, block.id)
        if entity_id is not None:
            self.entity_id = "." + slugify(id_prefix + "_" + entity_id + prefix)
            self._unique_id += "_" + slugify(entity_id)
        self._name = block.type_name()
        if conf.get(CONF_SHOW_ID_IN_NAME):
            self._name += " [" + block.id + "]"
        self._block = block
        self.hass = hass
        self._block.cb_updated.append(self._updated)
        block.shelly_device = self
        self._name = _get_specific_config(conf, CONF_NAME, self.name, block.id)              
        self._is_removed = False

    @property
    def name(self):
        """Return the display name of this device."""
        return self._name

    def _updated(self, _block):
        """Receive events when the switch state changed (by mobile,
        switch etc)"""

        if self.entity_id is not None and not self._is_removed:
            self.schedule_update_ha_state(True)

    @property
    def device_state_attributes(self):
        """Show state attributes in HASS"""
        attrs = {'ip_address': self._block.ip_addr,
                 'shelly_type': self._block.type_name(),
                 'shelly_id': self._block.id}

        if self._block.info_values is not None:
            for key, value in self._block.info_values.items():
                attrs[key] = value

        return attrs

    def remove(self):
        self._is_removed = True
        self.hass.add_job(self.async_remove)

class ShellyDevice(Entity):
    """Base class for Shelly entities"""

    def __init__(self, dev, hass):
        conf = hass.data[SHELLY_CONFIG]
        id_prefix = conf.get(CONF_OBJECT_ID_PREFIX)
        self._unique_id = id_prefix + "_" + dev.type + "_" + dev.id
        self.entity_id = "." + slugify(self._unique_id)
        entity_id = _get_specific_config(conf, CONF_ENTITY_ID , 
                                                    None, dev.id, dev.block.id)
        if entity_id is not None:
            self.entity_id = "." + slugify(id_prefix + "_" + entity_id)
            self._unique_id += "_" + slugify(entity_id)
        self._name = dev.type_name()
        if conf.get(CONF_SHOW_ID_IN_NAME):
            self._name += " [" + dev.id + "]"  # 'Test' #light.name
        self._dev = dev
        self.hass = hass
        self._dev.cb_updated.append(self._updated)
        dev.shelly_device = self
        self._name = _get_specific_config(conf, CONF_NAME, self._name, dev.id, dev.block.id)

        self._sensor_conf = _get_sensor_config(conf, dev.id, dev.block.id)

        self._is_removed = False

    def _updated(self, _block):
        """Receive events when the switch state changed (by mobile,
        switch etc)"""
        if self.entity_id is not None and not self._is_removed:
            self.schedule_update_ha_state(True)

        if self._dev.info_values is not None:
            for key, _value in self._dev.info_values.items():            
                ukey = self._dev.id + '-' + key
                if not ukey in DEVICE_SENSORS:
                    DEVICE_SENSORS.append(ukey)
                    for sensor in self._sensor_conf:
                        if SENSOR_TYPES[sensor].get('attr') == key:
                            attr = {'sensor_type':key,
                                    SHELLY_DEVICE_ID : _get_device_key(self._dev)}
                            conf = self.hass.data[SHELLY_CONFIG]
                            discovery.load_platform(self.hass, 'sensor',
                                                    DOMAIN, attr, conf)
    @property
    def name(self):
        """Return the display name of this device."""
        return self._name

    @property
    def device_state_attributes(self):
        """Show state attributes in HASS"""
        attrs = {'ip_address': self._dev.ip_addr,
                 'shelly_type': self._dev.type_name(),
                 'shelly_id': self._dev.id}

        if self._dev.block.info_values is not None:
            for key, value in self._dev.block.info_values.items():
                attrs[key] = value

        if self._dev.info_values is not None:
            for key, value in self._dev.info_values.items():
                attrs[key] = value

        if self._dev.sensor_values is not None:
            for key, value in self._dev.sensor_values.items():
                attrs[key] = value

        return attrs

    @property
    def unique_id(self):
        """Return the ID of this device."""
        return self._unique_id

    @property
    def available(self):
        """Return true if switch is available."""
        return self._dev.available()

    def remove(self):
        self._is_removed = True
        self.hass.add_job(self.async_remove)
