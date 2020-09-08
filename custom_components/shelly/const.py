"""
"""

from datetime import timedelta

from homeassistant.const import (
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_POWER,
    TEMP_CELSIUS,
    POWER_WATT,
    ENERGY_WATT_HOUR
)

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

#Debug settings used for testing
CONF_LOCAL_PY_SHELLY = 'debug_local_py_shelly'
CONF_ONLY_DEVICE_ID = 'debug_only_device_id'
CONF_DEBUG_ENABLE_INFO = 'debug_enable_info'

CONF_WIFI_SENSOR = 'wifi_sensor' #deprecated
CONF_UPTIME_SENSOR = 'uptime_sensor' #deprecated

DEFAULT_IGMPFIX = False
DEFAULT_DISCOVERY = True
DEFAULT_OBJECT_ID_PREFIX = 'shelly'
DEFAULT_SCAN_INTERVAL = 60 #timedelta(seconds=60)
DEFAULT_SHOW_ID_IN_NAME = False
DEFAULT_MDNS = True

DEFAULT_SETTINGS = \
{
    'default' : {},
    'temperature' : {CONF_UNIT:'°C'},
    'device_temp' : {CONF_UNIT:'°C'},
    'illuminance' : {CONF_UNIT:'lx'},
    'humidity' : {CONF_UNIT:'%'},
    'total_consumption' : {CONF_DECIMALS:2, CONF_DIV:1000, CONF_UNIT:'kWh'},
    'total_returned' : {CONF_DECIMALS:2, CONF_DIV:1000, CONF_UNIT:'kWh'},
    'current' : {CONF_UNIT:'A', CONF_DECIMALS:1},
    'current_consumption' : {CONF_UNIT:'W'},
    'voltage' : {CONF_UNIT:'V', CONF_DECIMALS:0},
    'power_factor' : {CONF_DECIMALS:1},
    'uptime': {CONF_DIV:3600, CONF_UNIT:'h'},
    'rssi': {CONF_UNIT:'dB'},
    'tilt': {CONF_UNIT:'°'},
    'battery': {CONF_UNIT:'%'},
    'ppm': {CONF_UNIT:'PPM'},
    'total_work_time': {CONF_DIV:3600, CONF_UNIT:'h'},
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
ATTRIBUTE_ILLUMINANCE = 'illuminance'
ATTRIBUTE_PPM = 'ppm'
ATTRIBUTE_SENSOR = 'sensor'
ATTRIBUTE_TOTAL_WORK_TIME = 'total_work_time'

ALL_ATTRIBUTES = {
    ATTRIBUTE_IP_ADDRESS,
    ATTRIBUTE_SHELLY_TYPE,
    ATTRIBUTE_SHELLY_ID,
    ATTRIBUTE_SSID,
    ATTRIBUTE_RSSI,
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
    ATTRIBUTE_ILLUMINANCE,
    ATTRIBUTE_PPM,
    ATTRIBUTE_SENSOR,
    ATTRIBUTE_TOTAL_WORK_TIME
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
    ATTRIBUTE_CLOUD_STATUS,
    ATTRIBUTE_SWITCH,
    ATTRIBUTE_OVER_POWER,
    ATTRIBUTE_OVER_TEMP,
    ATTRIBUTE_TOTAL_CONSUMPTION,
    ATTRIBUTE_VOLTAGE,
    ATTRIBUTE_BATTERY,
    ATTRIBUTE_CLICK_CNT,
    ATTRIBUTE_CLICK_TYPE,
    ATTRIBUTE_TILT,
    ATTRIBUTE_VIBRATION,
    ATTRIBUTE_TEMPERATURE,
    ATTRIBUTE_ILLUMINANCE,
    ATTRIBUTE_PPM,
    ATTRIBUTE_SENSOR,
    ATTRIBUTE_TOTAL_WORK_TIME
}

SENSOR_ALL = 'all'
SENSOR_RSSI = 'rssi'
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
SENSOR_DEV_TEMP = 'device_temp'
SENSOR_OVER_TEMP = 'over_temp'
SENSOR_CLOUD = 'cloud'
SENSOR_MQTT = 'mqtt'
SENSOR_BATTERY = 'battery'
SENSOR_SWITCH = 'switch'
SENSOR_CLICK_TYPE = 'click_type'
SENSOR_TILT = 'tilt'
SENSOR_VIBRATION = 'vibration'
SENSOR_TEMPERATURE = 'temperature'
SENSOR_ILLUMINANCE = 'illuminance'
SENSOR_PPM = 'ppm'
SENSOR_TOTAL_WORK_TIME = 'total_work_time'

ALL_SENSORS = {
    SENSOR_RSSI: {'attr':'rssi'},
    SENSOR_UPTIME: {'attr':'uptime'},
    SENSOR_OVER_POWER: {'attr':'over_power'},
    SENSOR_CURRENT_CONSUMPTION: {},
    SENSOR_TOTAL_CONSUMPTION: {'attr':'total_consumption'},
    SENSOR_TOTAL_RETURNED: {'attr':'total_returned'},
    SENSOR_DEV_TEMP: {'attr':'device_temp'},
    SENSOR_OVER_TEMP: {'attr':'over_temp'},
    SENSOR_CLOUD:  {'attr':'cloud_status'},
    SENSOR_MQTT:  {'attr':'mqtt_connected'},
    SENSOR_BATTERY : {'attr':'battery'},
    SENSOR_VOLTAGE : {'attr':'voltage'},
    SENSOR_POWER_FACTOR : {'attr':'power_factor'},
    SENSOR_CURRENT : {'attr':'current'},
    SENSOR_SWITCH : {},
    SENSOR_CLICK_TYPE : {'attr':'click_type'},
    SENSOR_TILT : {'attr':'tilt'},
    SENSOR_VIBRATION  : {'attr':'vibration'},
    SENSOR_TEMPERATURE : {'attr':'temperature'},
    SENSOR_ILLUMINANCE : {'attr':'illuminance'},
    SENSOR_PPM : {'attr':'ppm'},
    SENSOR_TOTAL_WORK_TIME : {'attr':'total_work_time'}
}

EXTRA_SENSORS = {
    SENSOR_ALL: {},
    SENSOR_POWER: {},
    SENSOR_CONSUMPTION: {}
}

DEFAULT_SENSORS = [
    SENSOR_CURRENT_CONSUMPTION,
    SENSOR_TOTAL_CONSUMPTION
]

SENSOR_TYPE_TEMPERATURE = 'temperature'
SENSOR_TYPE_HUMIDITY = 'humidity'
SENSOR_TYPE_POWER = 'current_consumption'
SENSOR_TYPE_RSSI = 'rssi'
SENSOR_TYPE_UPTIME = 'uptime'
SENSOR_TYPE_BATTERY = 'battery'
SENSOR_TYPE_OVER_POWER = 'over_power'
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
    SENSOR_TYPE_UPTIME:
        ['Uptime', 's', 'mdi:timer-outline', None, None],
    SENSOR_TYPE_BATTERY:
        ['Battery', '%', None, DEVICE_CLASS_BATTERY, None],
    SENSOR_TYPE_OVER_POWER:
        ['Over power', '', 'mdi:flash-alert', None, 'bool'],
    SENSOR_TYPE_DEVICE_TEMP:
        ['Device temperature', TEMP_CELSIUS, "mdi:oil-temperature", None, None],
    SENSOR_TYPE_OVER_TEMP:
        ['Over temperature', '', 'mdi:alert', None, 'bool'],
    SENSOR_TYPE_CLOUD_STATUS:
        ['Cloud status', '', 'mdi:cloud-question', None, None],
    SENSOR_TYPE_MQTT_CONNECTED:
        ['MQTT connected', '', 'mdi:transit-connection-variant',
         DEVICE_CLASS_CONNECTIVITY, 'bool'],
    SENSOR_TYPE_FLOOD:
        ['Flood', '', 'mdi:water', None, 'bool'],
    SENSOR_TYPE_DOOR_WINDOW:
        ['Door/Window', '', 'mdi:door', 'window', 'bool'],
    SENSOR_TYPE_ILLUMINANCE:
        ['Illuminance', 'lux', None, DEVICE_CLASS_ILLUMINANCE, None],
    SENSOR_TYPE_TOTAL_CONSUMPTION:
        ['Total consumption', ENERGY_WATT_HOUR,
         'mdi:flash-circle', DEVICE_CLASS_POWER, None],
    SENSOR_TYPE_TOTAL_RETURNED:
        ['Total returned', ENERGY_WATT_HOUR,
         'mdi:flash-circle', DEVICE_CLASS_POWER, None],
    SENSOR_TYPE_VOLTAGE:
        ['Voltage', 'V', 'mdi:flash', None, None],
    SENSOR_TYPE_POWER_FACTOR:
        ['Power factor', None, 'mdi:flash', None, None],
    SENSOR_TYPE_CURRENT:
        ['Current', 'A', 'mdi:flash', None, None],
    SENSOR_TYPE_CLICK_TYPE:
        ['Click type', '', 'mdi:hockey-puck', None, None],
    SENSOR_TYPE_TILT:
        ['Tilt', '', 'mdi:angle-acute', None, None],
    SENSOR_TYPE_VIBRATION:
        ['Vibration', '', 'mdi:vibrate', None, 'bool'],
    SENSOR_TYPE_PPM:
        ['Concentration', 'PPM', 'mdi:gauge', None, None],
    SENSOR_TYPE_TOTAL_WORK_TIME:
        ['Total work time', 's', 'mdi:briefcase-clock', None, None],
}
