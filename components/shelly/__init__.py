"""Support for Shelly devices."""
import logging

import voluptuous as vol

from homeassistant.const import (
    CONF_DEVICES, CONF_DISCOVERY, CONF_ID, CONF_NAME, CONF_PASSWORD,
    CONF_USERNAME, EVENT_HOMEASSISTANT_STOP)
from homeassistant.helpers import discovery
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

REQUIREMENTS = ['pyShelly==0.0.22']

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'shelly'

CONF_IGMPFIX = 'igmp_fix'
CONF_SHOW_ID_IN_NAME = 'show_id_in_name'
CONF_OBJECT_ID_PREFIX = 'id_prefix'
CONF_LIGHT_SWITCH = 'light_switch'
CONF_VERSION = 'version'

DEFAULT_IGMPFIX = False
DEFAULT_DISCOVERY = True
DEFAULT_SHOW_ID_IN_NAME = True
DEFAULT_OBJECT_ID_PREFIX = 'shelly'

SHELLY_DATA = 'shellyData'
SHELLY_CONFIG = 'shellyCfg'

__version__ = "0.0.6"
VERSION = __version__

DEVICE_SCHEMA = vol.Schema({
    vol.Required(CONF_ID): cv.string,
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_LIGHT_SWITCH, default=False): cv.boolean,
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_IGMPFIX, default=DEFAULT_IGMPFIX): cv.boolean,
        vol.Optional(CONF_SHOW_ID_IN_NAME,
                     default=DEFAULT_SHOW_ID_IN_NAME): cv.boolean,
        vol.Optional(CONF_DISCOVERY, default=DEFAULT_DISCOVERY): cv.boolean,
        vol.Optional(CONF_OBJECT_ID_PREFIX,
                     default=DEFAULT_OBJECT_ID_PREFIX): cv.string,
        vol.Optional(CONF_USERNAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_DEVICES, default=[]): vol.All(cv.ensure_list,
                                                        [DEVICE_SCHEMA]),
        vol.Optional(CONF_VERSION, default=False): cv.boolean,
    })
}, extra=vol.ALLOW_EXTRA)


def get_device_config(conf, device_id):
    """Get config for device."""
    device_conf_list = conf.get(CONF_DEVICES)
    for item in device_conf_list:
        if item[CONF_ID] == device_id:
            return item
    return {}


def setup(hass, config):
    """Setup Shelly component"""
    _LOGGER.info("Starting shelly, %s", __version__)

    conf = config.get(DOMAIN, {})
    hass.data[SHELLY_CONFIG] = conf

    discover = conf.get(CONF_DISCOVERY)

    from pyShelly import pyShelly

    devices = []

    def _device_added(dev, code):
        devices.append(dev)
        device_config = get_device_config(conf, dev.id)
        if not discover and device_config == {}:
            return
        data_key = SHELLY_DATA + dev.id + dev.devType
        hass.data[data_key] = dev
        attr = {'dataKey': data_key}
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

    def _device_removed(dev, code):
        dev.shelly_device.async_remove()
        devices.remove(dev)

    # def _deviceAddFilter(id, devType, addr):
    #    if discover:
    #        return True
    #    devConf = getDeviceConfig(conf, id)
    #    if devConf != {}:
    #        return True

    pys = pyShelly()
    _LOGGER.info("pyShelly, %s", pys.version())
    pys.cb_deviceAdded = _device_added
    pys.cb_deviceRemoved = _device_removed
    # pys.cb_deviceAddFilter = _deviceAddFilter
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
        _LOGGER.info("Shutting down Xiaomi Hub")
        pys.close()

    hass.bus.listen_once(EVENT_HOMEASSISTANT_STOP, stop_shelly)

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
        return {'ipaddr': self._dev.ipaddr,
                'shelly_type': self._dev.typeName(),
                'shelly_id': self._dev.id}

    @property
    def unique_id(self):
        """Return the ID of this device."""
        return self._unique_id

    @property
    def available(self):
        """Return true if switch is available."""
        return self._dev.available()
