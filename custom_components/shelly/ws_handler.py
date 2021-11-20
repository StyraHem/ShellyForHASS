"""WebSocket for Shelly."""
# pylint: disable=unused-argument
# from typing_extensions import Required
import os
import voluptuous as vol
from homeassistant.components import websocket_api
import homeassistant.helpers.config_validation as cv
from .const import (
    CONF_UNIT, ALL_ATTRIBUTES, ALL_SENSORS, DEFAULT_SETTINGS, DOMAIN,
    CONF_DECIMALS, CONF_DIV, CONF_SETTINGS, ALL_CONFIG, GLOBAL_CONFIG, DEBUG_CONFIG, DEVICE_CONFIG)
import json

async def setup_ws(instance):
    """Set up WS API handlers."""
    hass = instance.hass
    websocket_api.async_register_command(hass, shelly_config)
    websocket_api.async_register_command(hass, shelly_get_config)
    websocket_api.async_register_command(hass, shelly_setting)

@websocket_api.async_response
@websocket_api.websocket_command({vol.Required("type"): "s4h/get_config"})
async def shelly_get_config(hass, connection, msg):
    #print("GET CONFIG*****************")
    """Handle get config command."""
    content = {}
    content["type"] = 's4h/get_config' #Debug
    instances = []
    for entity_id, instance in hass.data[DOMAIN].items():
        options = {}
        options['name'] = instance.config_entry.title
        options['instance_id'] = entity_id
        #options['conf'] = json.dumps(instance.conf, sort_keys=True,
        #                             indent=4, separators=(',', ': '))
        settings = []
        cfgAttr = instance.conf.get("attributes",[])
        cfgSensor = instance.conf.get("sensors",[])
        ALL = ALL_SENSORS.keys() | ALL_ATTRIBUTES
        conf_settings = instance.conf.get(CONF_SETTINGS, {})
        for id in ALL:
            attr = id in cfgAttr
            sensor = id in cfgSensor
            conf_setting = conf_settings.get(id, {})
            unit = conf_setting.get(CONF_UNIT, "")
            div = conf_setting.get(CONF_DIV, "")
            decimals = conf_setting.get(CONF_DECIMALS, "")
            image = cfgSensor[sensor][2] if sensor else ""
            default = DEFAULT_SETTINGS.get(id, {})
            settings.append({'id': id,
                             'name': id,
                             'image': image,
                             'has' : {
                                'sensor' : id in ALL_SENSORS,
                                'attrib' : id in ALL_ATTRIBUTES,
                                'decimals' : CONF_DECIMALS in default,
                                'div' : CONF_DIV in default,
                                'unit' : CONF_UNIT in default
                             },
                             'value': {                                 
                                'sensor':sensor,
                                'attrib':attr,
                                'unit':unit,
                                'div':div,
                                'decimals':decimals
                             },
                             'default' : {
                                'decimals': default.get(CONF_DECIMALS),
                                'div': default.get(CONF_DIV),
                                'unit': default.get(CONF_UNIT)
                             }
                            })
        settings.sort(key=lambda x: x.get('name'))
        options["settings"] = settings
        configs = []
        config_list = GLOBAL_CONFIG
        if (os.getenv("SHELLY_DEBUG")):
            config_list = GLOBAL_CONFIG + DEBUG_CONFIG
        for key in config_list:
            value = ALL_CONFIG[key]
            if "type" in value:
                configs.append( {
                    "id" : key,
                    "name" : key,
                    "type" : value["type"],
                    "value" : instance.conf.get(key, ''),
                    "default" : value.get('def', '')
                })
        options["configs"]=configs
        instances.append(options)

    content["instances"] = instances
    connection.send_message(websocket_api.result_message(msg["id"], content))

@websocket_api.async_response
@websocket_api.websocket_command({
    vol.Required("type"): "s4h/setting",
    vol.Required("data"): vol.Schema({
        vol.Required("id"): cv.string,
        vol.Required("param"): cv.string,
        vol.Required("value"): cv.string,
        vol.Required("instanceid") : cv.string
    })
})
async def shelly_setting(hass, connection, msg):
    """Handle set setting config command."""
    data = msg['data']
    instance_id = data['instanceid']
    instance = hass.data[DOMAIN][instance_id]
    param = data['param']
    id = data['id']
    value = data['value'] 
    if param=="attrib":
        instance.set_config_attribute(id, value=="True")
    if param=="sensor":
        instance.set_config_sensor(id, value=="True")
    if param in ("decimals", "div"):
        instance.set_setting(id, param, int(value) if value!="" else None)
    if param in ("unit"):
        instance.set_setting(id, param, value if value!="" else None)

@websocket_api.async_response
@websocket_api.websocket_command({
    vol.Required("type"): "s4h/config",
    vol.Required("data"): vol.Schema({
        vol.Required("id"): cv.string,
        vol.Required("value"): cv.string,
        vol.Required("instanceid") : cv.string
    })
})
async def shelly_config(hass, connection, msg):
    """Handle set setting config command."""
    data = msg['data']
    instance_id = data['instanceid']
    instance = hass.data[DOMAIN][instance_id]
    id = data['id']
    cfg = ALL_CONFIG[id]    
    if cfg.get('type')=="bool":
        value = data['value']=="True"
    elif cfg.get('type')=="int":
        value = int(data['value'])
    else:
        value = data['value'] 
    instance.set_config(id, value)
