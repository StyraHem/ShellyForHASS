"""WebSocket for Shelly."""
# pylint: disable=unused-argument
# from typing_extensions import Required
from distutils.log import debug
import os
import voluptuous as vol
from homeassistant.components import websocket_api
import homeassistant.helpers.config_validation as cv
from .const import (
    CONF_OBJECT_ID_PREFIX, CONF_UNIT, ALL_ATTRIBUTES, ALL_SENSORS, DEFAULT_SETTINGS, DOMAIN,
    CONF_DECIMALS, CONF_DIV, CONF_SETTINGS, ALL_CONFIG, GLOBAL_CONFIG, DEBUG_CONFIG, DEVICE_CONFIG)
import json
from homeassistant.helpers.translation import async_get_translations

async def setup_ws(instance):
    """Set up WS API handlers."""
    hass = instance.hass
    websocket_api.async_register_command(hass, shelly_config)
    websocket_api.async_register_command(hass, shelly_get_config)
    websocket_api.async_register_command(hass, shelly_setting)
    websocket_api.async_register_command(hass, shelly_convert)

@websocket_api.async_response
@websocket_api.websocket_command({vol.Required("type"): "s4h/get_config", vol.Required("language", default="en"): cv.string})
async def shelly_get_config(hass, connection, msg):
    app = hass.data[DOMAIN]
    resources = await async_get_translations(
        hass,
        msg["language"],
        'frontend',
        {'shelly'} if app.is_ver('2022.6.0') else 'shelly'
    )
    #print("GET CONFIG*****************")
    """Handle get config command."""
    content = {}
    content["type"] = 's4h/get_config' #Debug
    instances = []
    for entity_id, instance in app.instances.items():
        options = {}
        options['yaml'] = instance.config_entry.source=='import' and not instance.config_entry.options
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
            default = DEFAULT_SETTINGS.get(id, {})
            base = "component.shelly.frontend.settings." + id
            title = resources.get(base, id)

            settings.append({'id': id,
                             'title': title,                            
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
        settings.sort(key=lambda x: x.get('title'))
        options["settings"] = settings
        configs = []
        config_list = GLOBAL_CONFIG
        if (os.getenv("SHELLY_DEBUG")):
            config_list = GLOBAL_CONFIG + DEBUG_CONFIG
        for key in config_list:
            value = ALL_CONFIG[key]
            base = "component.shelly.frontend.config." + key + "."
            name = resources.get(base + "title", key)
            desc = resources.get(base + "desc")
            group = value.get("group")
            group = resources.get("component.shelly.frontend.config.groups." + group, group)
            if "type" in value:
                configs.append( {
                    "id" : key,
                    "title" : name,
                    "desc" : desc,
                    "group": group,
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
    instance = hass.data[DOMAIN].instances[instance_id]
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
    instance = hass.data[DOMAIN].instances[instance_id]
    id = data['id']
    cfg = ALL_CONFIG[id]    
    if cfg.get('type')=="bool":
        value = data['value']=="True"
    elif cfg.get('type')=="int":
        value = int(data['value'])
    else:
        value = data['value'] 
    instance.set_config(id, value)

@websocket_api.async_response
@websocket_api.websocket_command({
    vol.Required("type"): "s4h/convert",
    vol.Required("data"): vol.Schema({
        vol.Required("instanceid") : cv.string
    })
})
async def shelly_convert(hass, connection, msg):
    "Convert config.yaml to integration"
    data = msg['data']
    instance_id = data['instanceid']
    instance = hass.data[DOMAIN].instances[instance_id]
    system_options = instance.conf.copy()
    data = {}
    data[CONF_OBJECT_ID_PREFIX] = \
        system_options.pop(CONF_OBJECT_ID_PREFIX, "shelly")
    instance.hass.config_entries.async_update_entry(
        instance.config_entry, data=data
    )
    entry = instance.hass.config_entries.async_get_entry(instance_id)
    if (entry.title=="config.yaml"):
        entry.title="Shelly"
    instance.hass.config_entries.async_update_entry(entry, options=system_options)