"""
Shelly block.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""

from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.util import slugify #, dt as dt_util
from homeassistant.const import CONF_NAME

from .const import (CONF_OBJECT_ID_PREFIX, CONF_ENTITY_ID,
                    CONF_SHOW_ID_IN_NAME, DOMAIN)

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
        self._show_id_in_name = conf.get(CONF_SHOW_ID_IN_NAME)
        self._block = block
        self.hass = instance.hass
        self.instance = instance
        self._block.cb_updated.append(self._updated)
        block.shelly_device = self  #todo, should be array??
        self._name = instance._get_specific_config(CONF_NAME, None, block.id)
        self._name_ext = None
        self._is_removed = False
        self.async_on_remove(self._remove_handler)
        self._master_unit = False
        self._settings = instance.get_settings(block.id)

    def _remove_handler(self):
        self._is_removed = True
        self._block.cb_updated.remove(self._updated)

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
        disabled = self.registry_entry and self.registry_entry.disabled_by
        if self.entity_id is not None and not self._is_removed \
            and not disabled:
            self.schedule_update_ha_state(True)

    @property
    def device_state_attributes(self):
        """Show state attributes in HASS"""
        attrs = {'shelly_type': self._block.type_name(),
                 'shelly_id': self._block.id,
                 'ip_address': self._block.ip_addr
                }

        room = self._block.room_name()
        if room:
            attrs['room'] = room

        if self._master_unit:

            attrs['protocols'] = self._block.protocols

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

    @property
    def unique_id(self):
        """Return the ID of this device."""
        return self._unique_id

    def remove(self):
        self._is_removed = True
        self.hass.add_job(self.async_remove)

    @property
    def available(self):
        """Return true if switch is available."""
        return self._block.available()
