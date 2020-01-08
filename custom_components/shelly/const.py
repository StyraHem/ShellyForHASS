"""
"""

from datetime import timedelta

DOMAIN = 'shelly'

CONF_ADDITIONAL_INFO = 'additional_information'
CONF_IGMPFIX = 'igmp_fix'
CONF_MDNS = 'mdns'
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
CONF_CLOUD_AUTH_KEY = 'cloud_auth_key'
CONF_CLOUD_SEREVR = 'cloud_server'
CONF_TMPL_NAME = 'tmpl_name'
CONF_DISCOVER_BY_IP = 'discover_by_ip'
CONF_HOST_IP = 'host_ip'

CONF_WIFI_SENSOR = 'wifi_sensor' #deprecated
CONF_UPTIME_SENSOR = 'uptime_sensor' #deprecated

DEFAULT_IGMPFIX = False
DEFAULT_DISCOVERY = True
DEFAULT_OBJECT_ID_PREFIX = 'shelly'
DEFAULT_SCAN_INTERVAL = timedelta(seconds=60)
DEFAULT_SHOW_ID_IN_NAME = True
DEFAULT_MDNS = True

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