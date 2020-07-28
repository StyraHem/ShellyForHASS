"""Shelly Configuration Schemas."""
# pylint: disable=dangerous-default-value
from homeassistant.const import (
    CONF_DEVICES, CONF_DISCOVERY, CONF_ID, CONF_NAME, CONF_PASSWORD,
    CONF_SCAN_INTERVAL, CONF_USERNAME, EVENT_HOMEASSISTANT_STOP)
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from .const import *

ALL_SENSORS_W_EXTRA = list(ALL_SENSORS.keys()) + list(EXTRA_SENSORS.keys())

SENSOR_SCHEMA = vol.Schema({
    vol.Optional(CONF_NAME): cv.string,
})


SETTING_SCHEMA = vol.Schema({
    vol.Optional(CONF_DECIMALS): cv.positive_int,
    vol.Optional(CONF_DIV): cv.positive_int,
    vol.Optional(CONF_UNIT): cv.string
})

SETTINGS_SCHEMA = vol.Schema({
    vol.Optional('temperature'): SETTING_SCHEMA,
    vol.Optional('humidity'): SETTING_SCHEMA,
    vol.Optional('illuminance'): SETTING_SCHEMA,
    vol.Optional('current'): SETTING_SCHEMA,
    vol.Optional('total_consumption'): SETTING_SCHEMA,
    vol.Optional('total_returned'): SETTING_SCHEMA,
    vol.Optional('current_consumption'): SETTING_SCHEMA,
    vol.Optional('device_temp'): SETTING_SCHEMA,
    vol.Optional('voltage'): SETTING_SCHEMA,
    vol.Optional('power_factor'): SETTING_SCHEMA,
    vol.Optional('uptime'): SETTING_SCHEMA,
    vol.Optional('rssi'): SETTING_SCHEMA
})

DEVICE_SCHEMA = vol.Schema({
    vol.Required(CONF_ID): cv.string,
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_LIGHT_SWITCH, default=False): cv.boolean,
    vol.Optional(CONF_SENSORS):
        vol.All(cv.ensure_list, [vol.In(ALL_SENSORS_W_EXTRA)]),
    vol.Optional(CONF_UPGRADE_SWITCH): cv.boolean,
    vol.Optional(CONF_UNAVALABLE_AFTER_SEC) : cv.positive_int,
    vol.Optional(CONF_ENTITY_ID): cv.string,
    vol.Optional(CONF_POWER_DECIMALS): cv.positive_int, #deprecated
    vol.Optional(CONF_SETTINGS, default={}): SETTINGS_SCHEMA
})

STEP_SCHEMA = vol.Schema({
    vol.Optional(CONF_OBJECT_ID_PREFIX,
                 default=DEFAULT_OBJECT_ID_PREFIX): str,
})

CONFIG_SCHEMA_ROOT = vol.Schema({
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
        vol.Optional(CONF_UPGRADE_SWITCH, default=True): cv.boolean,
        vol.Optional(CONF_UNAVALABLE_AFTER_SEC, default=90) : cv.positive_int,
        vol.Optional(CONF_SENSORS, default=DEFAULT_SENSORS):
                     vol.All(cv.ensure_list, [vol.In(ALL_SENSORS_W_EXTRA)]),
        vol.Optional(CONF_ATTRIBUTES, default=list(DEFAULT_ATTRIBUTES)):
                     vol.All(cv.ensure_list,
                                [vol.In(ALL_ATTRIBUTES | EXTRA_ATTRIBUTES)]),
        vol.Optional(CONF_ADDITIONAL_INFO,
                     default=True): cv.boolean,
        vol.Optional(CONF_SCAN_INTERVAL,
                     default=DEFAULT_SCAN_INTERVAL): cv.positive_int,
        vol.Optional(CONF_POWER_DECIMALS): cv.positive_int, #deprecated
        vol.Optional(CONF_LOCAL_PY_SHELLY,
                     default=False): cv.boolean,
        vol.Optional(CONF_ONLY_DEVICE_ID) : cv.string,
        vol.Optional(CONF_CLOUD_AUTH_KEY) : cv.string,
        vol.Optional(CONF_CLOUD_SERVER) : cv.string,
        vol.Optional(CONF_TMPL_NAME) : cv.string,
        vol.Optional(CONF_DISCOVER_BY_IP, default=[]):
                     vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(CONF_MDNS, default=DEFAULT_MDNS): cv.boolean,
        vol.Optional(CONF_HOST_IP, default='') : cv.string,
        vol.Optional(CONF_SETTINGS, default={}): SETTINGS_SCHEMA,
        vol.Optional(CONF_MQTT_PORT, default=0): cv.positive_int
    })

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: CONFIG_SCHEMA_ROOT
}, extra=vol.ALLOW_EXTRA)
