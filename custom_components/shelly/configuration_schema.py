"""Shelly Configuration Schemas."""
# pylint: disable=dangerous-default-value
from homeassistant.const import (
    CONF_DEVICES, CONF_DISCOVERY, CONF_ID, CONF_NAME, CONF_PASSWORD,
    CONF_SCAN_INTERVAL, CONF_USERNAME, EVENT_HOMEASSISTANT_STOP)
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from .const import *

SENSOR_SCHEMA = vol.Schema({
    vol.Optional(CONF_NAME): cv.string,
})

DEVICE_SCHEMA = vol.Schema({
    vol.Required(CONF_ID): cv.string,
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_LIGHT_SWITCH, default=False): cv.boolean,
    vol.Optional(CONF_SENSORS):
            vol.All(cv.ensure_list, [vol.In(ALL_SENSORS)]),
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
        vol.Optional(CONF_SENSORS, default=DEFAULT_SENSORS):
                        vol.All(cv.ensure_list, [vol.In(ALL_SENSORS)]),
        vol.Optional(CONF_ATTRIBUTES, default=list(DEFAULT_ATTRIBUTES)):
                        vol.All(cv.ensure_list,
                                [vol.In(ALL_ATTRIBUTES | EXTRA_ATTRIBUTES)]),
        vol.Optional(CONF_ADDITIONAL_INFO,
                     default=True): cv.boolean,
        vol.Optional(CONF_SCAN_INTERVAL,
                     default=DEFAULT_SCAN_INTERVAL): cv.time_period,
        vol.Optional(CONF_POWER_DECIMALS): cv.positive_int,
        vol.Optional(CONF_LOCAL_PY_SHELLY,
                     default=False): cv.boolean,
        vol.Optional(CONF_ONLY_DEVICE_ID) : cv.string,
        vol.Optional(CONF_CLOUD_AUTH_KEY) : cv.string,
        vol.Optional(CONF_CLOUD_SEREVR) : cv.string,
        vol.Optional(CONF_TMPL_NAME) : cv.string,
        vol.Optional(CONF_DISCOVER_BY_IP, default=[]):
                        vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(CONF_MDNS, default=DEFAULT_MDNS): cv.boolean,
        vol.Optional(CONF_HOST_IP, default='') : cv.string,
    })
}, extra=vol.ALLOW_EXTRA)
