"""
Support for Shelly smart home devices.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/shelly/
"""
# pylint: disable=broad-except, bare-except, invalid-name, import-error

from datetime import timedelta, datetime
import logging
import time
import pytz
import asyncio
import voluptuous as vol

from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.const import (
    CONF_DEVICES, CONF_DISCOVERY, CONF_ID, CONF_NAME, CONF_PASSWORD,
    CONF_SCAN_INTERVAL, CONF_USERNAME, EVENT_HOMEASSISTANT_STOP)
from homeassistant import config_entries
from homeassistant.helpers import discovery
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.helpers.restore_state import RestoreStateData
from homeassistant.helpers.entity_registry import ATTR_RESTORED
from homeassistant.helpers.entity import Entity
from homeassistant.util import slugify, dt as dt_util

from .const import *
from .configuration_schema import CONFIG_SCHEMA

REQUIREMENTS = ['pyShelly==0.1.19']

_LOGGER = logging.getLogger(__name__)

__version__ = "0.1.6"
VERSION = __version__

BLOCK_SENSORS = []  #Keep track dynamic block sensors is added
DEVICE_SENSORS = []  #Keep track dynamic device sensors is added

async def async_setup(hass, config):
    """Set up this integration using yaml."""
    if DOMAIN not in config:
        return True
    hass.data[DOMAIN] = config
    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_IMPORT}, data={}
        )
    )
    return True

async def async_setup_entry(hass, config_entry):

    """Setup Shelly component"""
    _LOGGER.info("Starting shelly, %s", __version__)
    config = hass.data[DOMAIN]
    conf = config.get(DOMAIN, {})

    hass.data[SHELLY_CONFIG] = conf

    if conf.get(CONF_WIFI_SENSOR) is not None:
        _LOGGER.warning("wifi_sensor is deprecated, use rssi in sensors instead.")
        if conf.get(CONF_WIFI_SENSOR) and SENSOR_RSSI not in conf[CONF_SENSORS]:
            conf[CONF_SENSORS].append(SENSOR_RSSI)

    if conf.get(CONF_UPTIME_SENSOR) is not None:
        _LOGGER.warning("uptime_sensor is deprecated, use uptime in sensors instead.")
        if conf.get(CONF_UPTIME_SENSOR) and SENSOR_UPTIME not in conf[CONF_SENSORS]:
            conf[CONF_SENSORS].append(SENSOR_UPTIME)

    hass.data["SHELLY_INSTANCE"] = ShellyInstance(hass, config_entry, conf)

    #def update_status_information():
    #    pys.update_status_information()
        #for _, block in pys.blocks.items():
        #    block.update_status_information()

    #async def update_domain_callback(_now):
    #    """Update the Shelly status information"""
    #    await hass.async_add_executor_job(update_status_information)

    #if conf.get(CONF_ADDITIONAL_INFO):
    #    hass.helpers.event.async_track_time_interval(
    #        update_domain_callback, update_interval)

    return True

class ShellyInstance():
    """Config instance of Shelly"""

    def __init__(self, hass, config_entry, conf):
        self.hass = hass
        self.config_entry = config_entry
        self.platforms = {}
        self.pys = None
        self.conf = conf
        self.discover = conf.get(CONF_DISCOVERY)

        self.conf_attributes = set(conf.get(CONF_ATTRIBUTES))
        if ATTRIBUTE_ALL in self.conf_attributes:
            self.conf_attributes |= ALL_ATTRIBUTES
        if ATTRIBUTE_DEFAULT in self.conf_attributes:
            self.conf_attributes |= DEFAULT_ATTRIBUTES
        if ATTRIBUTE_SWITCH in self.conf_attributes:
            self.conf_attributes.add(ATTRIBUTE_SWITCH + "_1")
            self.conf_attributes.add(ATTRIBUTE_SWITCH + "_2")
        if ATTRIBUTE_CONSUMPTION in self.conf_attributes:
            self.conf_attributes.add(ATTRIBUTE_CURRENT_CONSUMPTION)
            self.conf_attributes.add(ATTRIBUTE_TOTAL_CONSUMPTION)

        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, self._stop)

        hass.loop.create_task(
            self.start_up()
        )

    async def start_up(self):
        conf = self.conf
        if conf.get(CONF_LOCAL_PY_SHELLY):
            _LOGGER.info("Loading local pyShelly")
            #pylint: disable=no-name-in-module
            from .pyShelly import pyShelly
        else:
            from pyShelly import pyShelly

        additional_info = conf.get(CONF_ADDITIONAL_INFO)
        update_interval = conf.get(CONF_SCAN_INTERVAL)

        self.pys = pys = pyShelly()
        _LOGGER.info("pyShelly, %s", pys.version())
        pys.cb_block_added.append(self._block_added)
        pys.cb_device_added.append(self._device_added)
        pys.cb_device_removed.append(self._device_removed)
        pys.username = conf.get(CONF_USERNAME)
        pys.password = conf.get(CONF_PASSWORD)
        pys.cloud_auth_key = conf.get(CONF_CLOUD_AUTH_KEY)
        pys.cloud_server = conf.get(CONF_CLOUD_SEREVR)
        pys.tmpl_name = conf.get(CONF_TMPL_NAME, pys.tmpl_name)
        if additional_info:
            pys.update_status_interval = update_interval
        pys.only_device_id = conf.get(CONF_ONLY_DEVICE_ID)
        pys.igmp_fix_enabled = conf.get(CONF_IGMPFIX)
        pys.mdns_enabled = conf.get(CONF_MDNS)
        pys.host_ip = conf.get(CONF_HOST_IP, '')
        pys.start()
        pys.discover()

        discover_by_ip = conf.get(CONF_DISCOVER_BY_IP)
        for ip_addr in discover_by_ip:
            pys.add_device_by_ip(ip_addr, 'IP-addr')

        if conf.get(CONF_VERSION):
            attr = {'version': VERSION, 'pyShellyVersion': pys.version()}
            self.add_device("sensor", attr)

        #Remove entities that have change type
        entity_reg = \
            await self.hass.helpers.entity_registry.async_get_registry()
        entities_to_remove = []
        restore_expired = dt_util.as_utc(datetime.now()) - timedelta(hours=12)
        for entity in entity_reg.entities.values():
            if entity.platform == "shelly":
                if entity.entity_id.startswith("sensor.") and \
                  (entity.entity_id.endswith("_switch") or \
                     entity.entity_id.endswith("_door_window") or \
                     entity.entity_id.endswith("_flood") or \
                     entity.entity_id.endswith("_mqtt_connected_attr") or \
                     entity.entity_id.endswith("_over_temp_attr") or \
                     entity.entity_id.endswith("_over_power_attr") \
                  ):
                    entities_to_remove.append(entity.entity_id)
                if entity.entity_id.startswith("sensor.") and \
                    entity.entity_id.endswith("_consumption") and \
                    not entity.entity_id.endswith("total_consumption") and \
                    not entity.entity_id.endswith("current_consumption"):
                    entities_to_remove.append(entity.entity_id)
                if entity.entity_id.startswith("binary_sensor.") and \
                   entity.entity_id.endswith("_cloud_status_attr"):
                    entities_to_remove.append(entity.entity_id)
                if entity.entity_id.startswith("switch.") and \
                   entity.entity_id.endswith("_firmware_update"):
                    entities_to_remove.append(entity.entity_id)
                if "_shdw_" in entity.entity_id or \
                   "_shwt_" in entity.entity_id or \
                   "_shht_" in entity.entity_id:
                    #todo check last_seen
                    data = await RestoreStateData.async_get_instance(self.hass)
                    if entity.entity_id in data.last_states:
                        data = data.last_states[entity.entity_id]
                        last_seen = dt_util.as_utc(data.last_seen)
                        if last_seen > restore_expired:
                            state = data.state
                            attr = dict(state.attributes)
                            attr[ATTR_RESTORED] = True
                            self.hass.states.async_set(entity.entity_id, \
                                                        state.state, attr)

        for entity_id in entities_to_remove:
            entity_reg.async_remove(entity_id)


    async def _stop(self, _):
        """Stop Shelly."""
        _LOGGER.info("Shutting down Shelly")
        self.pys.close()

    def _get_specific_config_root(self, key, *ids):
        item = self._get_specific_config(key, None, *ids)
        if item is None:
            item = self.conf.get(key)
        return item

    def _find_device_config(self, device_id):
        device_conf_list = self.conf.get(CONF_DEVICES)
        for item in device_conf_list:
            if item[CONF_ID].upper() == device_id:
                return item
        return None

    def _get_device_config(self, device_id, id_2=None):
        """Get config for device."""
        item = self._find_device_config(device_id)
        if item is None and id_2 is not None:
            item = self._find_device_config(id_2)
        if item is None:
            return {}
        return item

    def _get_specific_config(self, key, default, *ids):
        for device_id in ids:
            item = self._find_device_config(device_id)
            if item is not None and key in item:
                return item[key]
        return default

    def _get_sensor_config(self, *ids):
        sensors = self._get_specific_config(CONF_SENSORS, None, *ids)
        if sensors is None:
            sensors = self.conf.get(CONF_SENSORS)
        if sensors is None:
            return {}
        if SENSOR_ALL in sensors:
            return [*ALL_SENSORS.keys()]
        return sensors

    def conf_attribute(self, key):
        return key in self.conf_attributes

    def add_device(self, platform, dev):
        self.hass.add_job(self._asyncadd_device(platform, dev))

    async def _asyncadd_device(self, platform, dev):
        if platform not in self.platforms:
            self.platforms[platform] = asyncio.Event()
            await self.hass.config_entries.async_forward_entry_setup(
                    self.config_entry, platform)
            self.platforms[platform].set()

        await self.platforms[platform].wait()
        async_dispatcher_send(self.hass, "shelly_new_" + platform \
                                , dev, self)

    def _block_updated(self, block):
        hass_data = block.hass_data

        if hass_data['discover']:
            if hass_data['allow_upgrade_switch']:
                has_update = block.info_values.get('has_firmware_update', False)
                update_switch = getattr(block, 'firmware_switch', None)
                if has_update:
                    if update_switch is None:
                        attr = {'firmware': True, 'block':block}
                        self.add_device("switch", attr)
                elif update_switch is not None:
                    update_switch.remove()

            #block_key = _get_block_key(block)
            for key, _value in block.info_values.items():
                ukey = block.id + '-' + key
                if not ukey in BLOCK_SENSORS:
                    BLOCK_SENSORS.append(ukey)
                    for sensor in hass_data['sensor_cfg']:
                        if ALL_SENSORS[sensor].get('attr') == key:
                            attr = {'sensor_type':key,
                                    'itm': block}
                            if key in SENSOR_TYPES_CFG and \
                                SENSOR_TYPES_CFG[key][4] == 'bool':
                                self.add_device("binary_sensor", attr)
                            else:
                                self.add_device("sensor", attr)

    def _block_added(self, block):
        self.hass.add_job(self._async_block_added(block))

    async def _async_block_added(self, block):
        block.cb_updated.append(self._block_updated)
        discover_block = self.discover \
                         or self._get_device_config(block.id) != {}

        block.hass_data = {
            'allow_upgrade_switch' :
                self._get_specific_config_root(CONF_UPGRADE_SWITCH, block.id),
            'sensor_cfg' : self._get_sensor_config(block.id),
            'discover': discover_block
        }

        #Config block
        if block.unavailable_after_sec is None:
            block.unavailable_after_sec \
                = self._get_specific_config_root(CONF_UNAVALABLE_AFTER_SEC,
                                            block.id)

        # dev_reg = await self.hass.helpers.device_registry.async_get_registry()
        # dev_reg.async_get_or_create(
        #     config_entry_id=block.id,
        #     identifiers={(DOMAIN, block.id)},
        #     manufacturer="Allterco",
        #     name=block.friendly_name(),
        #     model=block.type_name(),
        #     sw_version=block.fw_version(),
        # )
        #if conf.get(CONF_ADDITIONAL_INFO):
            #block.update_status_information()
            # cfg_sensors = conf.get(CONF_SENSORS)
            # for sensor in cfg_sensors:
            #     sensor_type = ALL_SENSORS[sensor]
            #     if 'attr' in sensor_type:
            #         attr = {'sensor_type':sensor_type['attr'],
            #                 SHELLY_BLOCK_ID : block_key}
            #         discovery.load_platform(hass, 'sensor', DOMAIN, attr,
            #                                 config)

    def _device_added(self, dev, _code):
        self.hass.add_job(self._async_device_added(dev, _code))

    async def _async_device_added(self, dev, _code):
        device_config = self._get_device_config(dev.id, dev.block.id)
        if not self.discover and device_config == {}:
            return

        if dev.device_type == "ROLLER":
            self.add_device("cover", dev)
        if dev.device_type == "RELAY":
            if device_config.get(CONF_LIGHT_SWITCH):
                self.add_device("light", dev)
            else:
                self.add_device("switch", dev)
        elif dev.device_type == 'POWERMETER':
            sensor_cfg = self._get_sensor_config(dev.id, dev.block.id)
            if SENSOR_CURRENT_CONSUMPTION in sensor_cfg or \
                SENSOR_CONSUMPTION in sensor_cfg or \
                SENSOR_POWER in sensor_cfg: #POWER deprecated
                self.add_device("sensor", dev)
            if SENSOR_TOTAL_CONSUMPTION in sensor_cfg or \
                SENSOR_CONSUMPTION in sensor_cfg or \
                SENSOR_POWER in sensor_cfg: #POWER deprecated
                self.add_device("sensor", {'sensor_type' : 'total_consumption',
                                            'itm': dev})
        elif dev.device_type == 'SWITCH':
            sensor_cfg = self._get_sensor_config(dev.id, dev.block.id)
            if SENSOR_SWITCH in sensor_cfg:
                self.add_device("binary_sensor", dev)
        elif dev.device_type == "SENSOR":
            self.add_device("sensor", dev)
        elif dev.device_type == "BINARY_SENSOR":
            self.add_device("binary_sensor", dev)
        elif dev.device_type in ["LIGHT", "DIMMER"]:
            self.add_device("light", dev)

    def _device_removed(self, dev, _code):
        dev.shelly_device.remove()
        try:
            pass
            #key = _dev_key(dev)
            #del DEVICES[key]
        except KeyError:
            pass

class ShellyBlock(RestoreEntity):
    """Base class for Shelly entities"""

    def __init__(self, block, instance, prefix=""):
        conf = instance.conf
        id_prefix = conf.get(CONF_OBJECT_ID_PREFIX)
        self._unique_id = slugify(id_prefix + "_" + block.type + "_" +
                                  block.id + prefix)
        self.entity_id = "." + self._unique_id
        entity_id = \
            instance._get_specific_config(CONF_ENTITY_ID, None, block.id)
        if entity_id is not None:
            self.entity_id = "." + slugify(id_prefix + "_" + entity_id + prefix)
            self._unique_id += "_" + slugify(entity_id)
        #self._name = None
        #block.type_name()
        #if conf.get(CONF_SHOW_ID_IN_NAME):
        #    self._name += " [" + block.id + "]"
        self._show_id_in_name = conf.get(CONF_SHOW_ID_IN_NAME)
        self._block = block
        self.hass = instance.hass
        self.instance = instance
        self._block.cb_updated.append(self._updated)
        block.shelly_device = self
        self._name = instance._get_specific_config(CONF_NAME, None, block.id)
        self._name_ext = None
        self._is_removed = False

        #self.hass.add_job(self.setup_device(block))

    # async def setup_device(self, block):
    #     dev_reg = await self.hass.helpers.device_registry.async_get_registry()
    #     dev_reg.async_get_or_create(
    #         config_entry_id=self.entity_id,
    #         identifiers={(DOMAIN, block.id)},
    #         manufacturer="Allterco",
    #         name=block.friendly_name(),
    #         model=block.type_name(),
    #         sw_version=block.fw_version(),
    #     )

    @property
    def name(self):
        """Return the display name of this device."""
        if self._name is None:
            name = self._block.friendly_name()
        else:
            name = self._name
        if self._name_ext:
            name += ' - ' + self._name_ext
        if self._show_id_in_name:
            name += " [" + self._block.id + "]"
        return name

    def _updated(self, _block):
        """Receive events when the switch state changed (by mobile,
        switch etc)"""

        if self.entity_id is not None and not self._is_removed:
            self.schedule_update_ha_state(True)

    @property
    def device_state_attributes(self):
        """Show state attributes in HASS"""
        attrs = {'ip_address': self._block.ip_addr,
                 'shelly_type': self._block.type_name(),
                 'shelly_id': self._block.id,
                 'discovery': self._block.discovery_src
                }

        room = self._block.room_name()
        if room:
            attrs['room'] = room

        if self._block.info_values is not None:
            for key, value in self._block.info_values.items():
                if self.instance.conf_attribute(key):
                    attrs[key] = value

        return attrs

    @property
    def device_info(self):
        return {
            'identifiers': {
                (DOMAIN, self._block.unit_id)
            },
            'name': self._block.friendly_name(),
            'manufacturer': 'Allterco',
            'model': self._block.type_name(),
            'sw_version': self._block.fw_version()
        }

        return self.instance.build_device_info(self._block)

    @property
    def unique_id(self):
        """Return the ID of this device."""
        return self._unique_id

    def remove(self):
        self._is_removed = True
        self.hass.add_job(self.async_remove)

class ShellyDevice(RestoreEntity):
    """Base class for Shelly entities"""

    def __init__(self, dev, instance):
        conf = instance.conf
        id_prefix = conf.get(CONF_OBJECT_ID_PREFIX)
        self._unique_id = id_prefix + "_" + dev.type + "_" + dev.id
        self.entity_id = "." + slugify(self._unique_id)
        entity_id = instance._get_specific_config(CONF_ENTITY_ID,
                                         None, dev.id, dev.block.id)
        if entity_id is not None:
            self.entity_id = "." + slugify(id_prefix + "_" + entity_id)
            self._unique_id += "_" + slugify(entity_id)
        self._show_id_in_name = conf.get(CONF_SHOW_ID_IN_NAME)
        self._name_ext = None
        #self._name = dev.type_name()
        #if conf.get(CONF_SHOW_ID_IN_NAME):
        #    self._name += " [" + dev.id + "]"  # 'Test' #light.name
        self._dev = dev
        self.hass = instance.hass
        self.instance = instance
        self._dev.cb_updated.append(self._updated)
        dev.shelly_device = self
        self._name = instance._get_specific_config(CONF_NAME, None,
                                          dev.id, dev.block.id)

        self._sensor_conf = instance._get_sensor_config(dev.id, dev.block.id)

        self._is_removed = False

    def _updated(self, _block):
        """Receive events when the switch state changed (by mobile,
        switch etc)"""
        if self.entity_id is not None and not self._is_removed:
            self.schedule_update_ha_state(True)

        if self._dev.info_values is not None:
            for key, _value in self._dev.info_values.items():
                ukey = self._dev.id + '-' + key
                if not ukey in DEVICE_SENSORS:
                    DEVICE_SENSORS.append(ukey)
                    for sensor in self._sensor_conf:
                        if ALL_SENSORS[sensor].get('attr') == key:
                            attr = {'sensor_type':key,
                                    'itm':self._dev}
                            if key in SENSOR_TYPES_CFG and \
                                SENSOR_TYPES_CFG[key][4] == 'bool':
                                self.instance.add_device("binary_sensor", attr)
                            else:
                                self.instance.add_device("sensor", attr)

    @property
    def name(self):
        """Return the display name of this device."""
        if self._name is None:
            name = self._dev.friendly_name()
        else:
            name = self._name
        if self._name_ext:
            name += ' - ' + self._name_ext
        if self._show_id_in_name:
            name += " [" + self._dev.id + "]"
        return name

    @property
    def device_state_attributes(self):
        """Show state attributes in HASS"""
        attrs = {'ip_address': self._dev.ip_addr,
                 'shelly_type': self._dev.type_name(),
                 'shelly_id': self._dev.id,
                 'discovery': self._dev.discovery_src
                }
        room = self._dev.room_name()
        if room:
            attrs['room'] = room

        if self._dev.block.info_values is not None:
            for key, value in self._dev.block.info_values.items():
                if self.instance.conf_attribute(key):
                    attrs[key] = value

        if self._dev.info_values is not None:
            for key, value in self._dev.info_values.items():
                if self.instance.conf_attribute(key):
                    attrs[key] = value

        if self._dev.sensor_values is not None:
            for key, value in self._dev.sensor_values.items():
                if self.instance.conf_attribute(key):
                    attrs[key] = value

        return attrs

    @property
    def device_info(self):
        return {
            'identifiers': {
                (DOMAIN, self._dev.block.id)
            },
            'name': self._dev.block.friendly_name(),
            'manufacturer': 'Allterco',
            'model': self._dev.type_name(),
            'sw_version': self._dev.fw_version()
        }

    @property
    def unique_id(self):
        """Return the ID of this device."""
        return self._unique_id

    @property
    def available(self):
        """Return true if switch is available."""
        return self._dev.available()

    def remove(self):
        self._is_removed = True
        self.hass.add_job(self.async_remove)

    @property
    def should_poll(self):
        """No polling needed."""
        return False
