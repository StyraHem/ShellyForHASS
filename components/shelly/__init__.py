# -*- coding: utf-8 -*-

import voluptuous as vol

import logging
from homeassistant.helpers import discovery
from homeassistant.helpers.discovery import load_platform
from homeassistant.const import (EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP,
                                 CONF_USERNAME, CONF_PASSWORD, CONF_DISCOVERY, CONF_NAME, 
                                 CONF_ID, CONF_DEVICES, CONF_DEVICE_CLASS )
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['pyShelly==0.0.22']  

DOMAIN = 'shelly'
SHELLY_DATA = 'shellyData'
SHELLY_CONFIG = 'shellyCfg'

CONF_IGMPFIX = 'igmpfix'
CONF_SHOW_ID_IN_NAME = 'showIdInName'
CONF_OBJECT_ID_PREFIX = 'objectIdPrefix'
CONF_LIGHT_SWITCH = 'lightSwitch'
CONF_VERSION = 'version'

DEFAULT_IGMPFIX = False
DEFAULT_DISCOVERY = True
DEFAULT_SHOW_ID_IN_NAME = True
DEFAULT_OBJECT_ID_PREFIX = 'shelly'

__version__ = "0.0.4"
VERSION = __version__

DEVICE_SCHEMA = vol.Schema({
    vol.Required(CONF_ID): cv.string,
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_LIGHT_SWITCH, default=False): cv.boolean,
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_IGMPFIX, default=DEFAULT_IGMPFIX): cv.boolean,
        vol.Optional(CONF_SHOW_ID_IN_NAME, default=DEFAULT_SHOW_ID_IN_NAME): cv.boolean,
        vol.Optional(CONF_DISCOVERY, default=DEFAULT_DISCOVERY): cv.boolean,
        vol.Optional(CONF_OBJECT_ID_PREFIX, default=DEFAULT_OBJECT_ID_PREFIX): cv.string,
        vol.Optional(CONF_USERNAME): cv.string,
        vol.Optional(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_DEVICES, default=[]): vol.All(cv.ensure_list, [DEVICE_SCHEMA]),
        vol.Optional(CONF_VERSION, default=False): cv.boolean,
    })
}, extra=vol.ALLOW_EXTRA)

def getDeviceConfig(conf, id):
    deviceConfList = conf.get(CONF_DEVICES)
    for item in deviceConfList: 
        if (item[CONF_ID] == id):
            return item
    return {}

def setup(hass, config):
    
    _LOGGER.info("Starting shelly, " + __version__)
    
    conf = config.get(DOMAIN, {})      
    discover = conf.get(CONF_DISCOVERY) 
    deviceConfList = conf.get(CONF_DEVICES) 
    
    hass.data[SHELLY_CONFIG] = conf
    
    try:
        from .pyShelly import pyShelly
    except:
        from pyShelly import pyShelly
    
    devices = []
            
    def _deviceAdded(dev, code):
        devices.append(dev)
        devConf = getDeviceConfig(conf, dev.id)
        if not discover and devConf == {}:
            return
        dataKey = SHELLY_DATA + dev.id + dev.devType
        hass.data[dataKey]=dev
        attr = { 'dataKey' : dataKey }
        if dev.devType=="ROLLER":
            discovery.load_platform(hass, 'cover', DOMAIN, attr, config)
        elif dev.devType=="RELAY":
            devConf = getDeviceConfig(conf, dev.id)
            if devConf.get(CONF_LIGHT_SWITCH):
                discovery.load_platform(hass, 'light', DOMAIN, attr, config)
            else:
                discovery.load_platform(hass, 'switch', DOMAIN, attr, config)            
        elif dev.devType=="SENSOR" or dev.devType=="POWERMETER":
            discovery.load_platform(hass, 'sensor', DOMAIN, attr, config)
        elif dev.devType=="LIGHT":
            discovery.load_platform(hass, 'light', DOMAIN, attr, config)
            
    def _deviceRemoved(dev, code): 
        dev._shellyDevice.async_remove()
        devices.remove(dev)
        
    #def _deviceAddFilter(id, devType, addr): 
    #    if discover:
    #        return True
    #    devConf = getDeviceConfig(conf, id)
    #    if devConf != {}:
    #        return True
        
    pys = pyShelly()
    _LOGGER.info("pyShelly, " + pys.version())
    pys.cb_deviceAdded = _deviceAdded
    pys.cb_deviceRemoved = _deviceRemoved
    #pys.cb_deviceAddFilter = _deviceAddFilter
    pys.username = conf.get(CONF_USERNAME)
    pys.password = conf.get(CONF_PASSWORD)
    pys.igmpFixEnabled =  conf.get(CONF_IGMPFIX) 
    pys.open()
    pys.discover()
         
    if conf.get(CONF_VERSION):
        attr = { 'version' : VERSION, 'pyShellyVersion' : pys.version() }    
        discovery.load_platform(hass, 'sensor', DOMAIN, attr, config)        

    return True
    
class ShellyDevice(object):

    def __init__(self, dev, hass):
        conf = hass.data[SHELLY_CONFIG]
        idPrefix = conf.get(CONF_OBJECT_ID_PREFIX)
        self._unique_id = idPrefix + "_" + dev.type + "_" + dev.id                        
        self.entity_id = "." + idPrefix + "_" + dev.type + "_" + dev.id        
        self._name = dev.typeName()
        if conf.get(CONF_SHOW_ID_IN_NAME):
            self._name += " [" + dev.id + "]" #'Test' #light.name            
        self._dev = dev
        self._hass = hass
        self._dev.cb_updated.append(self._updated)
        dev._shellyDevice = self
        devConf = getDeviceConfig(conf, dev.id)
        self._name = devConf.get(CONF_NAME, self._name)
    
    def _updated(self):
        pass
        
    @property
    def name(self):
        """Return the display name of this device."""
        return self._name
        
    @property
    def device_state_attributes(self):
        return { 'ipaddr' : self._dev.ipaddr, 'shelly_type' : self._dev.typeName(), 
                 'shelly_id': self._dev.id }

    @property
    def unique_id(self):
        """Return the ID of this device."""
        return self._unique_id

    @property
    def available(self):
        """Return true if switch is available."""
        return self._dev.available()