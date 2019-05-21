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

REQUIREMENTS = ['pyShelly==0.0.30']

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'shelly'

CONF_ADDITIONAL_INFO = 'additional_information'
CONF_IGMPFIX = 'igmp_fix'
CONF_LIGHT_SWITCH = 'light_switch'
CONF_OBJECT_ID_PREFIX = 'id_prefix'
CONF_SHOW_ID_IN_NAME = 'show_id_in_name'
CONF_UPTIME_SENSOR = 'uptime_sensor'
CONF_VERSION = 'version'
CONF_WIFI_SENSOR = 'wifi_sensor'
CONF_POWER_DECIMALS = 'power_decimals'

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

__version__ = "0.0.14"
VERSION = __version__

DEVICE_SCHEMA = vol.Schema({
    vol.Required(CONF_ID): cv.string,
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_LIGHT_SWITCH, default=False): cv.boolean,
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
        vol.Optional(CONF_WIFI_SENSOR,
                     default=False): cv.boolean,
        vol.Optional(CONF_UPTIME_SENSOR,
                     default=False): cv.boolean,
        vol.Optional(CONF_ADDITIONAL_INFO,
                     default=True): cv.boolean,
        vol.Optional(CONF_SCAN_INTERVAL,
                     default=DEFAULT_SCAN_INTERVAL): cv.time_period,
        vol.Optional(CONF_POWER_DECIMALS): cv.positive_int
    })
}, extra=vol.ALLOW_EXTRA)

BLOCKS = {}
DEVICES = {}

def _get_block_key(block):
    key = block.id
    if not key in BLOCKS:
        BLOCKS[key] = block
    return key

def get_block_from_hass(hass, discovery_info):
    """Get block from HASS"""
    key = discovery_info[SHELLY_BLOCK_ID]
    return hass.data[SHELLY_BLOCKS][key]  

def _get_device_key(dev):
    key = dev.id + dev.device_type
    if not key in DEVICES:
        DEVICES[key] = dev
    return key

def get_device_from_hass(hass, discovery_info):
    """Get device from HASS"""
    device_key = discovery_info[SHELLY_DEVICE_ID]
    return hass.data[SHELLY_DEVICES][device_key]  

def get_device_config(conf, device_id, device_id_2=None):
    """Get config for device."""
    device_conf_list = conf.get(CONF_DEVICES)
    for item in device_conf_list:
        if item[CONF_ID] == device_id:
            return item
    if device_id_2 is not None:
        return get_device_config(conf, device_id_2)
    return {}

def setup(hass, config):
    """Setup Shelly component"""
    _LOGGER.info("Starting shelly, %s", __version__)

    conf = config.get(DOMAIN, {})
    update_interval = conf.get(CONF_SCAN_INTERVAL)
    hass.data[SHELLY_CONFIG] = conf
    discover = conf.get(CONF_DISCOVERY)

    try:
        from .pyShelly import pyShelly
        _LOGGER.info("Loading local pyShelly")
    except ImportError:
        from pyShelly import pyShelly

    hass.data[SHELLY_DEVICES] = DEVICES
    hass.data[SHELLY_BLOCKS] = BLOCKS

    def _block_updated(block):
        has_update = block.info_values.get('has_update', False)

        #now = time.time()
        #if block.id == "5DBDD5" and (now // 10) % 2 == 0:
        #    has_update = True

        update_switch = getattr(block, 'firmware_switch', None)
        if has_update:
            if update_switch is None:
                config = hass.data[SHELLY_CONFIG]
                attr = {'firmware': True,
                        SHELLY_BLOCK_ID : _get_block_key(block)}
                discovery.load_platform(hass, 'switch', DOMAIN, attr, config)
        elif update_switch is not None:
            update_switch.remove()

    def _block_added(block):
        block.cb_updated.append(_block_updated)
        block_key = _get_block_key(block)

        if conf.get(CONF_ADDITIONAL_INFO):
            block.update_status_information()            
            if conf.get(CONF_WIFI_SENSOR):
                rssi_attr = {'rssi': True, SHELLY_BLOCK_ID : block_key}
                discovery.load_platform(hass, 'sensor', DOMAIN, rssi_attr,
                                        config)

            if conf.get(CONF_UPTIME_SENSOR):
                upt_attr = {'uptime': True, SHELLY_BLOCK_ID : block_key}
                discovery.load_platform(hass, 'sensor', DOMAIN, upt_attr,
                                        config)

    def _device_added(dev, _code):
        device_key = _get_device_key(dev)
        attr = {SHELLY_DEVICE_ID : device_key}

        device_config = get_device_config(conf, dev.id, dev.block.id)
        if not discover and device_config == {}:
            return

        if dev.device_type == "ROLLER":
            discovery.load_platform(hass, 'cover', DOMAIN, attr, config)
        elif dev.device_type == "RELAY":
            if device_config.get(CONF_LIGHT_SWITCH):
                discovery.load_platform(hass, 'light', DOMAIN, attr, config)
            else:
                discovery.load_platform(hass, 'switch', DOMAIN, attr, config)
        elif dev.device_type in ["SENSOR","POWERMETER","INFOSENSOR"]:
            discovery.load_platform(hass, 'sensor', DOMAIN, attr, config)
        elif dev.device_type == "LIGHT":
            discovery.load_platform(hass, 'light', DOMAIN, attr, config)

    def _device_removed(dev, _code):
        dev.shelly_device.async_remove()
        try:
            del DEVICES[dev.id]
        except IndexError:
            pass

    pys = pyShelly()
    _LOGGER.info("pyShelly, %s", pys.version())
    pys.cb_block_added.append(_block_added)
    pys.cb_device_added.append(_device_added)
    pys.cb_device_removed.append(_device_removed)
    pys.username = conf.get(CONF_USERNAME)
    pys.password = conf.get(CONF_PASSWORD)
    pys.igmp_fix_enabled = conf.get(CONF_IGMPFIX)
    pys.open()
    pys.discover()

    if conf.get(CONF_VERSION):
        attr = {'version': VERSION, 'pyShellyVersion': pys.version()}
        discovery.load_platform(hass, 'sensor', DOMAIN, attr, config)

    def stop_shelly():
        """Stop Shelly."""
        _LOGGER.info("Shutting down Shelly")
        pys.close()

    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, stop_shelly)

    def update_status_information():
        pys.update_status_information()
        #for _, block in pys.blocks.items():
        #    block.update_status_information()

    async def update_domain_callback(_now):
        """Update the Shelly status information"""
        await hass.async_add_executor_job(update_status_information)

    if conf.get(CONF_ADDITIONAL_INFO):
        hass.helpers.event.async_track_time_interval(
            update_domain_callback, update_interval)

    return True

class ShellyBlock(Entity):
    """Base class for Shelly entities"""

    def __init__(self, block, hass, prefix=""):
        conf = hass.data[SHELLY_CONFIG]
        id_prefix = conf.get(CONF_OBJECT_ID_PREFIX)
        self._unique_id = slugify(id_prefix + "_" + block.type + "_" +
                                  block.id + prefix)
        self.entity_id = "." + self._unique_id
        self._name = block.type_name()
        if conf.get(CONF_SHOW_ID_IN_NAME):
            self._name += " [" + block.id + "]"
        self._block = block
        self._hass = hass
        self._block.cb_updated.append(self._updated)
        block.shelly_device = self
        device_config = get_device_config(conf, block.id)
        self._name = device_config.get(CONF_NAME, self._name)
                      
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

    def remove(self):
        self._is_removed = True
        self._hass.add_job(self.async_remove)

class ShellyDevice(Entity):
    """Base class for Shelly entities"""

    def __init__(self, dev, hass):
        conf = hass.data[SHELLY_CONFIG]
        id_prefix = conf.get(CONF_OBJECT_ID_PREFIX)
        self._unique_id = id_prefix + "_" + dev.type + "_" + dev.id
        self.entity_id = "." + id_prefix + "_" + dev.type + "_" + dev.id
        self._name = dev.type_name()
        if conf.get(CONF_SHOW_ID_IN_NAME):
            self._name += " [" + dev.id + "]"  # 'Test' #light.name
        self._dev = dev
        self._hass = hass
        self._dev.cb_updated.append(self._updated)
        dev.shelly_device = self
        device_config = get_device_config(conf, dev.id, dev.block.id)
        self._name = device_config.get(CONF_NAME, self._name)

    def _updated(self, _block):
        """Receive events when the switch state changed (by mobile,
        switch etc)"""
        if self.entity_id is not None:
            self.schedule_update_ha_state(True)

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
        if self._dev.info_values is not None:
            def set_attr(name):
                value = self._dev.info_values.get(name)
                if value is not None:
                    attrs[name] = value
            attrs['rssi'] = self._dev.info_values.get('rssi', '-')
            attrs['ssid'] = self._dev.info_values.get('ssid', '-')
            attrs['uptime'] = self._dev.info_values.get('uptime')
            attrs['has_fw_update'] = self._dev.info_values.get('has_update', False)
            attrs['fw_version'] = self._dev.info_values.get('fw_version')
            if self._dev.info_values.get('new_fw_version') is not None:
                attrs['new_fw_version'] = self._dev.info_values.get(
                    'new_fw_version')
            attrs['cloud_connected'] = self._dev.info_values.get('cloud_connected')            
            set_attr('temperature')
            set_attr('over_temperature')
            set_attr('over_power')
        return attrs

    @property
    def unique_id(self):
        """Return the ID of this device."""
        return self._unique_id

    @property
    def available(self):
        """Return true if switch is available."""
        return self._dev.available()
