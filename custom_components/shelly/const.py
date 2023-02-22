"""
"""

from datetime import timedelta

from homeassistant.const import (
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_ENERGY,
    TEMP_CELSIUS,
    POWER_WATT,
    ENERGY_WATT_HOUR,
    CONF_NAME,
    CONF_SCAN_INTERVAL,
    CONF_DISCOVERY
)

DEVICE_CLASS_MOTION = 'motion'

from homeassistant.components.binary_sensor import (
    DEVICE_CLASS_CONNECTIVITY
)

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
CONF_UPGRADE_BETA_SWITCH = 'upgrade_beta_switch'
CONF_UNAVALABLE_AFTER_SEC = 'unavailable_after_sec'
CONF_CLOUD_AUTH_KEY = 'cloud_auth_key'
CONF_CLOUD_SERVER = 'cloud_server'
CONF_TMPL_NAME = 'tmpl_name'
CONF_DISCOVER_BY_IP = 'discover_by_ip'
CONF_HOST_IP = 'host_ip'
CONF_ATTRIBUTES = 'attributes'
CONF_SETTINGS = 'settings'
CONF_DECIMALS = 'decimals'
CONF_DIV = 'div'
CONF_UNIT = 'unit'
CONF_MQTT_PORT = 'mqtt_port'
CONF_MQTT_SERVER_HOST = 'mqtt_server_host'
CONF_MQTT_SERVER_PORT = 'mqtt_server_port'
CONF_MQTT_SERVER_USERNAME = 'mqtt_server_username'
CONF_MQTT_SERVER_PASSWORD = 'mqtt_server_password'

#Debug settings used for testing
CONF_LOCAL_PY_SHELLY = 'debug_local_py_shelly'
CONF_ONLY_DEVICE_ID = 'debug_only_device_id'
CONF_DEBUG_ENABLE_INFO = 'debug_enable_info'

CONF_WIFI_SENSOR = 'wifi_sensor' #deprecated
CONF_UPTIME_SENSOR = 'uptime_sensor' #deprecated

GLOBAL_CONFIG = [
    CONF_ADDITIONAL_INFO,
    CONF_IGMPFIX,
    CONF_MDNS,
    #CONF_OBJECT_ID_PREFIX
    CONF_SHOW_ID_IN_NAME,
    CONF_VERSION,
    CONF_UPGRADE_SWITCH,
    CONF_UPGRADE_BETA_SWITCH,
    CONF_SCAN_INTERVAL,
    CONF_UNAVALABLE_AFTER_SEC,
    CONF_CLOUD_AUTH_KEY,
    CONF_CLOUD_SERVER,
    CONF_TMPL_NAME,
    #CONF_DISCOVER_BY_IP,
    CONF_DISCOVERY,
    CONF_HOST_IP,
    CONF_MQTT_PORT,
    CONF_MQTT_SERVER_HOST,
    CONF_MQTT_SERVER_PORT,
    CONF_MQTT_SERVER_USERNAME,
    CONF_MQTT_SERVER_PASSWORD,
]

DEBUG_CONFIG = [
    CONF_LOCAL_PY_SHELLY,
    CONF_ONLY_DEVICE_ID,
    CONF_DEBUG_ENABLE_INFO,
]

DEVICE_CONFIG = [
    CONF_ENTITY_ID,
    CONF_NAME,
    CONF_LIGHT_SWITCH,
    CONF_UPGRADE_SWITCH,
    CONF_UPGRADE_BETA_SWITCH,
    CONF_UNAVALABLE_AFTER_SEC,
]

ALL_CONFIG = {
    #CONF_ENTITY_ID : { "type" : "str" },
    #CONF_LIGHT_SWITCH : { "type" : "bool" },
    #CONF_OBJECT_ID_PREFIX : { "type" : "str" },    
    #CONF_DISCOVER_BY_IP : { "type" : "list" },

    #General
    CONF_VERSION : { "type" : "bool", "group": "general" },
    CONF_UPGRADE_SWITCH : { "type" : "bool", "group": "general" },
    CONF_UPGRADE_BETA_SWITCH : { "type" : "bool", "group": "general" },
    CONF_ADDITIONAL_INFO : { "type" : "bool", "group": "general" },
    CONF_UNAVALABLE_AFTER_SEC : { "type" : "int", "group": "general" },
    CONF_SCAN_INTERVAL : { "type" : "int", "group" : "general" },

    #Discovery
    CONF_IGMPFIX : { "type" : "bool", "group": "discovery" },
    CONF_MDNS : { "type" : "bool", "group": "discovery"  },    
    CONF_DISCOVERY : { "type" : "bool", "group": "discovery"  },
    CONF_HOST_IP : { "type" : "str", "group": "discovery"  },
    
    #Name
    CONF_SHOW_ID_IN_NAME : { "type" : "bool", "group": "name" },
    CONF_TMPL_NAME : { "type" : "str", "group": "name"  },

    #Cloud
    CONF_CLOUD_AUTH_KEY : { "type" : "txt", "group": "cloud"  },
    CONF_CLOUD_SERVER : { "type" : "str", "group": "cloud"  },
    
    #MQTT integrated
    CONF_MQTT_PORT : { "type" : "int", "group" : "mqtt-integrated" },
    
    #MQTT broker
    CONF_MQTT_SERVER_HOST : { "type" : "str", "group" : "mqtt-broker" },
    CONF_MQTT_SERVER_PORT : { "type" : "int", "group" : "mqtt-broker" },
    CONF_MQTT_SERVER_USERNAME : { "type" : "str", "group" : "mqtt-broker" },
    CONF_MQTT_SERVER_PASSWORD : {"type" : "str", "group" : "mqtt-broker" },
    
    #Debug
    CONF_LOCAL_PY_SHELLY : { "type" : "bool", "group" : "debug" },
    CONF_ONLY_DEVICE_ID : {"type" : "str", "group" : "debug" },
    CONF_DEBUG_ENABLE_INFO : {"type" : "bool", "group" : "debug"}
}

DEFAULT_IGMPFIX = False
DEFAULT_DISCOVERY = True
DEFAULT_OBJECT_ID_PREFIX = 'shelly'
DEFAULT_SCAN_INTERVAL = 60 #timedelta(seconds=60)
DEFAULT_SHOW_ID_IN_NAME = False
DEFAULT_MDNS = True

DEFAULT_WH = {CONF_DECIMALS:2, CONF_DIV:1000, CONF_UNIT:'kWh'}
DEFAULT_W = {CONF_UNIT:'W', CONF_DECIMALS:0, CONF_DIV:1}
DEFAULT_TIME = {CONF_DIV:3600, CONF_UNIT:'h', CONF_DECIMALS:0}

DEFAULT_SETTINGS = \
{
    'default' : {},
    'temperature' : {CONF_UNIT:'°C', CONF_DECIMALS:0},
    'humidity' : {CONF_UNIT:'%'},
    'device_temp' : {CONF_UNIT:'°C', CONF_DECIMALS:0},
    'illuminance' : {CONF_UNIT:'lx'},
    'total_consumption' : DEFAULT_WH,
    'total_returned' : DEFAULT_WH,
    'current' : {CONF_UNIT:'A', CONF_DECIMALS:1},
    'current_consumption' : DEFAULT_W,
    'voltage' : {CONF_UNIT:'V', CONF_DECIMALS:0},
    'power_factor' : {CONF_DECIMALS:1},
    'uptime': DEFAULT_TIME,
    'rssi': {CONF_UNIT:'dB'},
    'tilt': {CONF_UNIT:'°'},
    'battery': {CONF_UNIT:'%'},
    'ppm': {CONF_UNIT:'PPM'},
    'total_work_time': DEFAULT_TIME,
    'position': {CONF_UNIT:'%'},
    'target_temperature': {CONF_UNIT:'°C', CONF_DECIMALS:1}
}

SHELLY_DEVICE_ID = 'device_id'
SHELLY_BLOCK_ID = 'block_id'

ATTRIBUTE_ALL = 'all'
ATTRIBUTE_DEFAULT = 'default'
ATTRIBUTE_IP_ADDRESS = 'ip_address'
ATTRIBUTE_SHELLY_TYPE = 'shelly_type'
ATTRIBUTE_SHELLY_ID = 'shelly_id'
ATTRIBUTE_SSID = 'ssid'
ATTRIBUTE_RSSI = 'rssi'
ATTRIBUTE_RSSI_LEVEL = 'rssi_level'
ATTRIBUTE_UPTIME = 'uptime'
ATTRIBUTE_HAS_FIRMWARE_UPDATE = 'has_firmware_update'
ATTRIBUTE_LATEST_FW = 'latest_fw_version'
ATTRIBUTE_LATEST_BETA_FW = 'latest_beta_fw_version'
ATTRIBUTE_FW = 'firmware_version'
ATTRIBUTE_CLOUD_ENABLED = 'cloud_enabled'
ATTRIBUTE_CLOUD_CONNECTED = 'cloud_connected'
ATTRIBUTE_MQTT_CONNECTED = 'mqtt_connected'
ATTRIBUTE_CLOUD_STATUS = 'cloud_status'
ATTRIBUTE_SWITCH = 'switch'
ATTRIBUTE_CONSUMPTION = 'consumption'
ATTRIBUTE_TOTAL_CONSUMPTION = 'total_consumption'
ATTRIBUTE_TOTAL_RETURNED = 'total_returned'
ATTRIBUTE_CURRENT_CONSUMPTION = 'current_consumption'
ATTRIBUTE_OVER_POWER = 'over_power'
ATTRIBUTE_OVER_VOLTAGE = 'over_voltage'
ATTRIBUTE_DEV_TEMP = 'device_temp'
ATTRIBUTE_OVER_TEMP = 'over_temp'
ATTRIBUTE_BATTERY = 'battery'
ATTRIBUTE_VOLTAGE = 'voltage'
ATTRIBUTE_PAYLOAD = 'payload'
ATTRIBUTE_CURRENT = 'current'
ATTRIBUTE_POWER_FACTOR = 'power_factor'
ATTRIBUTE_CLICK_TYPE = 'click_type'
ATTRIBUTE_CLICK_CNT = 'click_count'
ATTRIBUTE_TILT = 'tilt'
ATTRIBUTE_VIBRATION = 'vibration'
ATTRIBUTE_TEMPERATURE = 'temperature'
ATTRIBUTE_HUMIDITY = 'humidity'
ATTRIBUTE_ILLUMINANCE = 'illuminance'
ATTRIBUTE_PPM = 'ppm'
ATTRIBUTE_SENSOR = 'sensor'
ATTRIBUTE_TOTAL_WORK_TIME = 'total_work_time'
ATTRIBUTE_POSITION = 'position'

ALL_ATTRIBUTES = {
    ATTRIBUTE_IP_ADDRESS,
    ATTRIBUTE_SHELLY_TYPE,
    ATTRIBUTE_SHELLY_ID,
    ATTRIBUTE_SSID,
    ATTRIBUTE_RSSI,
    ATTRIBUTE_RSSI_LEVEL,
    ATTRIBUTE_UPTIME,
    ATTRIBUTE_HAS_FIRMWARE_UPDATE,
    ATTRIBUTE_LATEST_FW,
    ATTRIBUTE_LATEST_BETA_FW,
    ATTRIBUTE_FW,
    ATTRIBUTE_MQTT_CONNECTED,
    ATTRIBUTE_CLOUD_STATUS,
    ATTRIBUTE_SWITCH,
    ATTRIBUTE_TOTAL_CONSUMPTION,
    ATTRIBUTE_TOTAL_RETURNED,
    ATTRIBUTE_CURRENT_CONSUMPTION,
    ATTRIBUTE_VOLTAGE,
    ATTRIBUTE_OVER_POWER,
    ATTRIBUTE_OVER_VOLTAGE,
    ATTRIBUTE_DEV_TEMP,
    ATTRIBUTE_OVER_TEMP,
    ATTRIBUTE_BATTERY,
    ATTRIBUTE_CURRENT,
    ATTRIBUTE_POWER_FACTOR,
    ATTRIBUTE_CLICK_CNT,
    ATTRIBUTE_CLICK_TYPE,
    ATTRIBUTE_TILT,
    ATTRIBUTE_VIBRATION,
    ATTRIBUTE_TEMPERATURE,
    ATTRIBUTE_HUMIDITY,
    ATTRIBUTE_ILLUMINANCE,
    ATTRIBUTE_PPM,
    ATTRIBUTE_SENSOR,
    ATTRIBUTE_TOTAL_WORK_TIME,
    ATTRIBUTE_POSITION
}

EXTRA_ATTRIBUTES = {
    ATTRIBUTE_ALL,
    ATTRIBUTE_DEFAULT,
    ATTRIBUTE_CONSUMPTION,
    ATTRIBUTE_CLOUD_ENABLED,
    ATTRIBUTE_CLOUD_CONNECTED,
    ATTRIBUTE_PAYLOAD
}

DEFAULT_ATTRIBUTES = {
    ATTRIBUTE_IP_ADDRESS,
    ATTRIBUTE_SHELLY_TYPE,
    ATTRIBUTE_SHELLY_ID,
    ATTRIBUTE_HAS_FIRMWARE_UPDATE,
    #ATTRIBUTE_RSSI_LEVEL,
    ATTRIBUTE_CLOUD_STATUS,
    ATTRIBUTE_SWITCH,
    ATTRIBUTE_OVER_POWER,
    ATTRIBUTE_OVER_VOLTAGE,
    ATTRIBUTE_OVER_TEMP,
    ATTRIBUTE_TOTAL_CONSUMPTION,
    #ATTRIBUTE_VOLTAGE,
    ATTRIBUTE_BATTERY,
    ATTRIBUTE_CLICK_CNT,
    ATTRIBUTE_CLICK_TYPE,
    ATTRIBUTE_TILT,
    ATTRIBUTE_VIBRATION,
    ATTRIBUTE_TEMPERATURE,
    ATTRIBUTE_ILLUMINANCE,
    ATTRIBUTE_PPM,
    ATTRIBUTE_SENSOR,
    ATTRIBUTE_TOTAL_WORK_TIME,
    ATTRIBUTE_POSITION
}

SENSOR_ALL = 'all'
SENSOR_DEFAULT = 'default'
SENSOR_RSSI = 'rssi'
SENSOR_RSSI_LEVEL = 'rssi_level'
SENSOR_POWER = 'power'  #depreated, same as consumption
SENSOR_CONSUMPTION = 'consumption'
SENSOR_CURRENT_CONSUMPTION = 'current_consumption'
SENSOR_TOTAL_CONSUMPTION = 'total_consumption'
SENSOR_TOTAL_RETURNED = 'total_returned'
SENSOR_VOLTAGE = 'voltage'
SENSOR_POWER_FACTOR = 'power_factor'
SENSOR_CURRENT = 'current'
SENSOR_UPTIME = 'uptime'
SENSOR_OVER_POWER = 'over_power'
SENSOR_OVER_VOLTAGE = 'over_voltage'
SENSOR_DEV_TEMP = 'device_temp'
SENSOR_OVER_TEMP = 'over_temp'
SENSOR_CLOUD = 'cloud'
SENSOR_CLOUD_STATUS = 'cloud_status'
SENSOR_MQTT = 'mqtt'
SENSOR_MQTT_CONNECTED = 'mqtt_connected'
SENSOR_BATTERY = 'battery'
SENSOR_SWITCH = 'switch'
SENSOR_CLICK_TYPE = 'click_type'
SENSOR_TILT = 'tilt'
SENSOR_VIBRATION = 'vibration'
SENSOR_TEMPERATURE = 'temperature'
SENSOR_HUMIDITY = 'humidity'
SENSOR_ILLUMINANCE = 'illuminance'
SENSOR_PPM = 'ppm'
SENSOR_TOTAL_WORK_TIME = 'total_work_time'
SENSOR_POSITION = 'position'
SENSOR_TARGET_TEMP = 'target_temperature'

ALL_SENSORS = {
    SENSOR_RSSI: {'attr':'rssi'},
    SENSOR_RSSI_LEVEL: {'attr':'rssi_level'},
    SENSOR_UPTIME: {'attr':'uptime'},
    SENSOR_OVER_POWER: {'attr':'over_power'},
    SENSOR_OVER_VOLTAGE: {'attr':'over_voltage'},
    SENSOR_CURRENT_CONSUMPTION: {},
    SENSOR_TOTAL_CONSUMPTION: {'attr':'total_consumption'},
    SENSOR_TOTAL_RETURNED: {'attr':'total_returned'},
    SENSOR_DEV_TEMP: {'attr':'device_temp'},
    SENSOR_OVER_TEMP: {'attr':'over_temp'},
    SENSOR_CLOUD_STATUS:  {'attr':'cloud_status'},
    SENSOR_MQTT_CONNECTED:  {'attr':'mqtt_connected'},
    SENSOR_BATTERY : {'attr':'battery'},
    SENSOR_VOLTAGE : {'attr':'voltage'},
    SENSOR_POWER_FACTOR : {'attr':'power_factor'},
    SENSOR_CURRENT : {'attr':'current'},
    SENSOR_SWITCH : {},
    SENSOR_CLICK_TYPE : {'attr':'click_type'},
    SENSOR_TILT : {'attr':'tilt'},
    SENSOR_VIBRATION  : {'attr':'vibration'},
    SENSOR_TEMPERATURE : {'attr':'temperature'},
    SENSOR_HUMIDITY : {'attr':'humidity'},
    SENSOR_ILLUMINANCE : {'attr':'illuminance'},
    SENSOR_PPM : {'attr':'ppm'},
    SENSOR_TOTAL_WORK_TIME : {'attr':'total_work_time'},
    SENSOR_POSITION : {'attr':'position'},
    SENSOR_TARGET_TEMP: {'attr':'target_temperature'},
}

EXTRA_SENSORS = {
    SENSOR_ALL: {},
    SENSOR_DEFAULT: {},
    SENSOR_POWER: {},
    SENSOR_CONSUMPTION: {},
    SENSOR_MQTT: {},
    SENSOR_CLOUD: {}
}

DEFAULT_SENSORS = [
    SENSOR_CURRENT_CONSUMPTION,
    SENSOR_TOTAL_CONSUMPTION,
    SENSOR_SWITCH,
    SENSOR_POSITION
]

SENSOR_TYPE_TEMPERATURE = 'temperature'
SENSOR_TYPE_HUMIDITY = 'humidity'
SENSOR_TYPE_POWER = 'current_consumption'
SENSOR_TYPE_RSSI = 'rssi'
SENSOR_TYPE_RSSI_LEVEL = 'rssi_level'
SENSOR_TYPE_UPTIME = 'uptime'
SENSOR_TYPE_BATTERY = 'battery'
SENSOR_TYPE_OVER_POWER = 'over_power'
SENSOR_TYPE_OVER_VOLTAGE = 'over_voltage'
SENSOR_TYPE_DEVICE_TEMP = 'device_temp'
SENSOR_TYPE_OVER_TEMP = 'over_temp'
SENSOR_TYPE_CLOUD_STATUS = 'cloud_status'
SENSOR_TYPE_MQTT_CONNECTED = 'mqtt_connected'
SENSOR_TYPE_SWITCH = 'switch'
SENSOR_TYPE_FLOOD = 'flood'
SENSOR_TYPE_DOOR_WINDOW = 'door_window'
SENSOR_TYPE_ILLUMINANCE = 'illuminance'
SENSOR_TYPE_TOTAL_CONSUMPTION = 'total_consumption'
SENSOR_TYPE_TOTAL_RETURNED = 'total_returned'
SENSOR_TYPE_VOLTAGE = 'voltage'
SENSOR_TYPE_POWER_FACTOR = 'power_factor'
SENSOR_TYPE_CURRENT = 'current'
SENSOR_TYPE_DEFAULT = 'default'
SENSOR_TYPE_CLICK_TYPE = 'click_type'
SENSOR_TYPE_VIBRATION = 'vibration'
SENSOR_TYPE_TILT = 'tilt'
SENSOR_TYPE_PPM = 'ppm'
SENSOR_TYPE_TOTAL_WORK_TIME = 'total_work_time'
SENSOR_TYPE_EXT_SWITCH = 'external_switch'
SENSOR_TYPE_MOTION = 'motion'
SENSOR_TYPE_POSITION = 'position'
SENSOR_TYPE_TARGET_TEMP = 'target_temperature'

SENSOR_TYPES_CFG = {
    SENSOR_TYPE_DEFAULT:
        [None, None, None, None, None],
    SENSOR_TYPE_TEMPERATURE:
        ['Temperature', TEMP_CELSIUS, None, DEVICE_CLASS_TEMPERATURE, None],
    SENSOR_TYPE_HUMIDITY:
        ['Humidity', '%', None, DEVICE_CLASS_HUMIDITY, None],
    SENSOR_TYPE_POWER:
        ['Consumption', POWER_WATT, 'mdi:flash-outline', None, None],
    SENSOR_TYPE_RSSI:
        ['RSSI', 'dB', 'mdi:wifi', None, None],
    SENSOR_TYPE_RSSI_LEVEL:
        ['RSSI Level', None, 'mdi:wifi', None, None],
    SENSOR_TYPE_UPTIME:
        ['Uptime', 's', 'mdi:timer-outline', None, None],
    SENSOR_TYPE_BATTERY:
        ['Battery', '%', None, DEVICE_CLASS_BATTERY, None],
    SENSOR_TYPE_OVER_POWER:
        ['Over power', None, 'mdi:flash-alert', None, 'bool'],
    SENSOR_TYPE_OVER_VOLTAGE:
        ['Over voltage', None, 'mdi:flash-alert', None, 'bool'],
    SENSOR_TYPE_DEVICE_TEMP:
        ['Device temperature', TEMP_CELSIUS, "mdi:oil-temperature", None, None],
    SENSOR_TYPE_OVER_TEMP:
        ['Over temperature', None, 'mdi:alert', None, 'bool'],
    SENSOR_TYPE_CLOUD_STATUS:
        ['Cloud status', None, 'mdi:cloud-question', None, None],
    SENSOR_TYPE_MQTT_CONNECTED:
        ['MQTT connected', None, 'mdi:transit-connection-variant',
         DEVICE_CLASS_CONNECTIVITY, 'bool'],
    SENSOR_TYPE_FLOOD:
        ['Flood', None, 'mdi:water', None, 'bool'],
    SENSOR_TYPE_DOOR_WINDOW:
        ['Door/Window', None, 'mdi:door', 'window', 'bool'],
    SENSOR_TYPE_ILLUMINANCE:
        ['Illuminance', 'lux', None, DEVICE_CLASS_ILLUMINANCE, None],
    SENSOR_TYPE_TOTAL_CONSUMPTION:
        ['Total consumption', ENERGY_WATT_HOUR,
         'mdi:lightning-bolt-circle', DEVICE_CLASS_ENERGY, None],
    SENSOR_TYPE_TOTAL_RETURNED:
        ['Total returned', ENERGY_WATT_HOUR,
         'mdi:lightning-bolt-circle', DEVICE_CLASS_ENERGY, None],
    SENSOR_TYPE_VOLTAGE:
        ['Voltage', 'V', 'mdi:alpha-v-circle-outline', None, None],
    SENSOR_TYPE_POWER_FACTOR:
        ['Power factor', '', 'mdi:flash', None, None],
    SENSOR_TYPE_CURRENT:
        ['Current', 'A', 'mdi:alpha-i-circle-outline', None, None],
    SENSOR_TYPE_CLICK_TYPE:
        ['Click type', None, 'mdi:light-switch', None, None],
    SENSOR_TYPE_TILT:
        ['Tilt', '', 'mdi:angle-acute', None, None],
    SENSOR_TYPE_VIBRATION:
        ['Vibration', None, 'mdi:vibrate', None, 'bool'],
    SENSOR_TYPE_PPM:
        ['Concentration', 'PPM', 'mdi:gauge', None, None],
    SENSOR_TYPE_TOTAL_WORK_TIME:
        ['Total work time', 's', 'mdi:briefcase-clock', None, None],
    SENSOR_TYPE_EXT_SWITCH:
        ['External switch', None, 'mdi:electric-switch', None, 'bool'],
    SENSOR_TYPE_MOTION:
        ['Motion', None, 'mdi:motion-sensor', DEVICE_CLASS_MOTION, 'bool'],
    SENSOR_TYPE_POSITION:
        ['Position', '', 'mdi:percent', None, None],
    SENSOR_TYPE_TARGET_TEMP:
        ['Target temperature', TEMP_CELSIUS, "mdi:target-variant", None, None],

}

