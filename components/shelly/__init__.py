"""Support for Shelly devices."""
from datetime import timedelta
import logging

import voluptuous as vol

from homeassistant.const import (
    CONF_DEVICES, CONF_DISCOVERY, CONF_ID, CONF_NAME, CONF_PASSWORD,
    CONF_SCAN_INTERVAL, CONF_USERNAME, EVENT_HOMEASSISTANT_STOP)
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

REQUIREMENTS = ['pyShelly==0.0.22']

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

DEFAULT_IGMPFIX = False
DEFAULT_DISCOVERY = True
DEFAULT_OBJECT_ID_PREFIX = 'shelly'
DEFAULT_SCAN_INTERVAL = timedelta(seconds=60)
DEFAULT_SHOW_ID_IN_NAME = True

SHELLY_DEVICES = 'shelly_devices'
SHELLY_CONFIG = 'shelly_cfg'
SHELLY_DEVICE_ID = 'device_id'

__version__ = "0.0.6"
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
                     default=DEFAULT_SCAN_INTERVAL): cv.time_period
    })
}, extra=vol.ALLOW_EXTRA)


def get_device_config(conf, device_id):
    """Get config for device."""
    device_conf_list = conf.get(CONF_DEVICES)
    for item in device_conf_list:
        if item[CONF_ID] == device_id:
            return item
    return {}
    
def get_device_from_hass(hass, discovery_info):
    device_key = discovery_info[SHELLY_DEVICE_ID]
    return hass.data[SHELLY_DEVICES][device_key]    

def setup(hass, config):
    """Setup Shelly component"""
    _LOGGER.info("Starting shelly, %s", __version__)

    conf = config.get(DOMAIN, {})
    update_interval = conf.get(CONF_SCAN_INTERVAL)
    hass.data[SHELLY_CONFIG] = conf    
    discover = conf.get(CONF_DISCOVERY)

    try:
        from .pyShelly import pyShelly  #Used for development only
    except:
        from pyShelly import pyShelly

    devices = {}
    block_sensors = {}
    hass.data[SHELLY_DEVICES] = devices

    def _device_added(dev, code):
        deviceKey = dev.id
        
        if deviceKey in devices:
            return            
        devices[deviceKey]=dev
        device_config = get_device_config(conf, dev.id)
        if not discover and device_config == {}:
            return

        #data_key = SHELLY_DATA + dev.id + dev.devType
        #hass.data[data_key] = dev
        attr = {SHELLY_DEVICE_ID : deviceKey}

        if conf.get(CONF_ADDITIONAL_INFO):
            dev.block.update_status_information()

        if dev.devType == "ROLLER":
            discovery.load_platform(hass, 'cover', DOMAIN, attr, config)
        elif dev.devType == "RELAY":
            device_config = get_device_config(conf, dev.id)
            if device_config.get(CONF_LIGHT_SWITCH):
                discovery.load_platform(hass, 'light', DOMAIN, attr, config)
            else:
                discovery.load_platform(hass, 'switch', DOMAIN, attr, config)
        elif dev.devType == "SENSOR" or dev.devType == "POWERMETER":
            discovery.load_platform(hass, 'sensor', DOMAIN, attr, config)
        elif dev.devType == "LIGHT":
            discovery.load_platform(hass, 'light', DOMAIN, attr, config)

        if conf.get(CONF_ADDITIONAL_INFO):
            if conf.get(CONF_WIFI_SENSOR) \
                    and block_sensors.get(dev.block.id + "_rssi") is None:
                rssi_attr = {'rssi': dev.infoValues.get('rssi'),
                             SHELLY_DEVICE_ID : deviceKey}
                discovery.load_platform(hass, 'sensor', DOMAIN, rssi_attr,
                                        config)
                block_sensors[dev.block.id + "_rssi"] = True

            if conf.get(CONF_UPTIME_SENSOR) \
                    and block_sensors.get(dev.block.id + "_uptime") is None:
                upt_attr = {'uptime': dev.infoValues.get('uptime'),
                            SHELLY_DEVICE_ID : deviceKey}
                discovery.load_platform(hass, 'sensor', DOMAIN, upt_attr,
                                        config)
                block_sensors[dev.block.id  + "_uptime"] = True

    def _device_removed(dev, code):
        dev.shelly_device.async_remove()
        try:
            del devices[dev.id]
        except:
            pass
        block_sensors[dev.dev.block.id + "_rssi"] = None
        block_sensors[dev.dev.block.id + "_uptime"] = None

    pys = pyShelly()
    _LOGGER.info("pyShelly, %s", pys.version())
    pys.cb_deviceAdded = _device_added
    pys.cb_deviceRemoved = _device_removed
    pys.username = conf.get(CONF_USERNAME)
    pys.password = conf.get(CONF_PASSWORD)
    pys.igmpFixEnabled = conf.get(CONF_IGMPFIX)
    pys.open()
    pys.discover()

    if conf.get(CONF_VERSION):
        attr = {'version': VERSION, 'pyShellyVersion': pys.version()}
        discovery.load_platform(hass, 'sensor', DOMAIN, attr, config)

    def stop_shelly(event):
        """Stop Shelly."""
        _LOGGER.info("Shutting down Shelly")
        pys.close()

    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, stop_shelly)

    def update_status_information():
        for _, block in pys.blocks.items():
            block.update_status_information()

    async def update_domain_callback(now):
        """Update the Shelly status information"""
        await hass.async_add_executor_job(update_status_information)

    if conf.get(CONF_ADDITIONAL_INFO):
        hass.helpers.event.async_track_time_interval(
            update_domain_callback, update_interval)

    return True


class ShellyDevice(Entity):
    """Base class for Shelly entities"""

    def __init__(self, dev, hass):
        conf = hass.data[SHELLY_CONFIG]
        id_prefix = conf.get(CONF_OBJECT_ID_PREFIX)
        self._unique_id = id_prefix + "_" + dev.type + "_" + dev.id
        self.entity_id = "." + id_prefix + "_" + dev.type + "_" + dev.id
        self._name = dev.typeName()
        if conf.get(CONF_SHOW_ID_IN_NAME):
            self._name += " [" + dev.id + "]"  # 'Test' #light.name
        self._dev = dev
        self._hass = hass
        self._dev.cb_updated.append(self._updated)
        dev.shelly_device = self
        device_config = get_device_config(conf, dev.id)
        self._name = device_config.get(CONF_NAME, self._name)

    def _updated(self):
        pass

    @property
    def name(self):
        """Return the display name of this device."""
        return self._name

    @property
    def device_state_attributes(self):
        attrs = {'ipaddr': self._dev.ipaddr,
                 'shelly_type': self._dev.typeName(),
                 'shelly_id': self._dev.id}
        if self._dev.infoValues is not None:
            attrs['rssi'] = self._dev.infoValues.get('rssi', '-')
            attrs['ssid'] = self._dev.infoValues.get('ssid', '-')
            attrs['uptime'] = self._dev.infoValues.get('uptime')
            attrs['has_update'] = self._dev.infoValues.get('has_update', False)
            attrs['fw_version'] = self._dev.infoValues.get('fw_version')
            if self._dev.infoValues.get('new_fw_version') is not None:
                attrs['new_fw_version'] = self._dev.infoValues.get(
                    'new_fw_version')
        return attrs

    @property
    def unique_id(self):
        """Return the ID of this device."""
        return self._unique_id

    @property
    def available(self):
        """Return true if switch is available."""
        return self._dev.available()
