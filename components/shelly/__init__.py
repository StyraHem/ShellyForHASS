# -*- coding: utf-8 -*-

import voluptuous as vol
import logging
from homeassistant.helpers import discovery
from homeassistant.helpers.discovery import load_platform
from homeassistant.const import (EVENT_HOMEASSISTANT_START, EVENT_HOMEASSISTANT_STOP)

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['pyShelly==0.0.19']

DOMAIN = 'shelly'
SHELLY_DATA = 'shellyData'
SHELLY_CONFIG = 'shellyCfg'

CONFIG_IGMPFIX = 'igmpfix'
DEFAULT_IGMPFIX = False
CONFIG_SHOW_ID_IN_NAME = 'showIdInName'
DEFAULT_SHOW_ID_IN_NAME = True
CONFIG_OBJECT_ID_PREFIX = 'objectIdPrefix'
DEFAULT_OBJECT_ID_PREFIX = 'shelly_'

__version__ = "0.0.2"
VERSION = __version__

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONFIG_IGMPFIX, default=DEFAULT_IGMPFIX): vol.Coerce(bool),
        vol.Optional(CONFIG_SHOW_ID_IN_NAME, default=DEFAULT_SHOW_ID_IN_NAME): vol.Coerce(bool),
        vol.Optional(CONFIG_OBJECT_ID_PREFIX, default=DEFAULT_OBJECT_ID_PREFIX): vol.Coerce(str),
    }),
}, extra=vol.ALLOW_EXTRA)

def setup(hass, config):
    
    _LOGGER.info("Starting shelly, " + __version__)
    
    conf = config.get(DOMAIN, {})      
    igmpfix = conf.get(CONFIG_IGMPFIX)    
    
    hass.data[SHELLY_CONFIG] = conf
    
    try:
        from .pyShelly import pyShelly
    except:
        from pyShelly import pyShelly
    
    devices = []

    def _deviceAdded(dev, code):
        devices.append(dev)
        dataKey = SHELLY_DATA + dev.id + dev.devType
        hass.data[dataKey]=dev
        attr = { 'dataKey' : dataKey }
        if dev.devType=="ROLLER":
            discovery.load_platform(hass, 'cover', DOMAIN, attr, config)
        elif dev.devType=="RELAY":
            discovery.load_platform(hass, 'switch', DOMAIN, attr, config)
        elif dev.devType=="SENSOR" or dev.devType=="POWERMETER":
            discovery.load_platform(hass, 'sensor', DOMAIN, attr, config)
        elif dev.devType=="LIGHT":
            discovery.load_platform(hass, 'light', DOMAIN, attr, config)
            
    def _deviceRemoved(dev, code): 
        dev._shellyDevice.async_remove()
        devices.remove(dev)
        
    pys = pyShelly()
    _LOGGER.info("pyShelly, " + pys.version())
    pys.cb_deviceAdded = _deviceAdded
    pys.cb_deviceRemoved = _deviceRemoved
    pys.igmpFixEnabled = igmpfix
    pys.open()
    pys.discover()
         
    return True
    
class ShellyDevice(object):

    def __init__(self, dev, hass):
        config = hass.data[SHELLY_CONFIG]
        idPrefix = config.get(CONFIG_OBJECT_ID_PREFIX)
        self._unique_id = idPrefix + dev.type + "_" + dev.id                        
        self.entity_id = "." + idPrefix + dev.type + "_" + dev.id        
        self._name = dev.typeName()
        if config.get(CONFIG_SHOW_ID_IN_NAME):
            self._name += " [" + dev.id + "]" #'Test' #light.name            
        self._dev = dev
        self._hass = hass
        self._dev.cb_updated.append(self._updated)
        dev._shellyDevice = self
    
    def _updated(self):
        pass
        
    @property
    def name(self):
        """Return the display name of this light."""
        return self._name
        
    @property
    def device_state_attributes(self):
        return { 'ipaddr' : self._dev.ipaddr, 'shelly_type' : self._dev.typeName() }

    @property
    def unique_id(self):
        """Return the ID of this device."""
        return self._unique_id

    @property
    def available(self):
        """Return true if switch is available."""
        return self._dev.available()
