"""
Shelly device.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""

from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import slugify
from homeassistant.const import CONF_NAME

from .const import (CONF_OBJECT_ID_PREFIX, CONF_ENTITY_ID, CONF_SHOW_ID_IN_NAME,
                    ALL_SENSORS, SENSOR_TYPES_CFG, DOMAIN)

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
        self._master_unit = False
        if hasattr(dev, 'master_unit') and dev.master_unit:
            self._master_unit = True

        self._settings = instance.get_settings(dev.id, dev.block.id)

    def _update_ha_state(self):        
        self.schedule_update_ha_state(True)

    def _updated(self, _block):
        """Receive events when the switch state changed (by mobile,
        switch etc)"""
        disabled = self.registry_entry and self.registry_entry.disabled_by
        if self.entity_id is not None and not self._is_removed and not disabled:
            
            self._update_ha_state()

        if self._dev.info_values is not None:
            device_sensors = self.instance.device_sensors
            for key, _value in self._dev.info_values.items():
                ukey = self._dev.id + '-' + key
                if not ukey in device_sensors:
                    device_sensors.append(ukey)
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

    def _debug_info(self, key, dev):
        if not self.instance._debug_msg:
            return ""
        dbg = ""
        if key in dev.info_values_coap:
            dbg += ", C=" + str(dev.info_values_coap[key])
        if key in dev.info_values_status:
            dbg += ", S=" + str(dev.info_values_status[key])
        return dbg

    def _debug_add_state_info(self, attrs):
        if not self.instance._debug_msg:
            return
        if self._dev.state_coap is not None:
            attrs['state_CoAP'] = self._dev.state_coap
        if self._dev.state_status is not None:
            attrs['state_RESTAPI'] = self._dev.state_status

    @property
    def device_state_attributes(self):
        """Show state attributes in HASS"""
        attrs = {'shelly_type': self._dev.type_name(),
                 'shelly_id': self._dev.id,
                 'ip_address': self._dev.ip_addr
                }

        self._debug_add_state_info(attrs)
        room = self._dev.room_name()
        if room:
            attrs['room'] = room

        if self._master_unit or self.instance._debug_msg:

            attrs['protocols'] = self._dev.protocols

            if self._dev.block.info_values is not None:
                info_values = self._dev.block.info_values.copy()
                for key, value in info_values.items():
                    if self.instance.conf_attribute(key):
                        settings = self._settings.get(key)
                        value = self.instance.format_value(settings, value, True)
                        key += self._debug_info(key, self._dev.block)
                        attrs[key] = value

        if self._dev.info_values is not None:
            for key, value in self._dev.info_values.items():
                if self.instance.conf_attribute(key):
                    settings = self._settings.get(key)
                    value = self.instance.format_value(settings, value, True)
                    key += self._debug_info(key, self._dev)
                    attrs[key] = value

        # if self._dev.sensor_values is not None:
        #     for key, value in self._dev.sensor_values.items():
        #         if self.instance.conf_attribute(key):
        #             settings = self._settings.get(key)
        #             value = self.instance.format_value(settings, value, True)
        #             attrs[key] = value

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
