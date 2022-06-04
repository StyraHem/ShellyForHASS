"""Adds config flow for Shelly."""
# pylint: disable=dangerous-default-value
import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from homeassistant.core import callback

from homeassistant.const import (
    CONF_PASSWORD, CONF_SCAN_INTERVAL, CONF_USERNAME
)
from .const import (CONF_LOCAL_PY_SHELLY, DOMAIN,
                    ALL_ATTRIBUTES, CONF_ATTRIBUTES,
                    ALL_SENSORS, CONF_SENSORS,
                    CONF_MDNS, CONF_VERSION, CONF_UPGRADE_SWITCH,
                    CONF_UPGRADE_BETA_SWITCH,
                    CONF_IGMPFIX, CONF_HOST_IP, CONF_MQTT_PORT,
                    CONF_CLOUD_AUTH_KEY, CONF_CLOUD_SERVER,
                    CONF_TMPL_NAME, CONF_ADDITIONAL_INFO,
                    CONF_OBJECT_ID_PREFIX,
                    CONF_UNAVALABLE_AFTER_SEC,
                    CONF_MQTT_SERVER_HOST, CONF_MQTT_SERVER_PORT,
                    CONF_MQTT_SERVER_USERNAME, CONF_MQTT_SERVER_PASSWORD
)
from .configuration_schema import STEP_SCHEMA

_LOGGER = logging.getLogger(__name__)

class ShellyFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for HA"""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        """Initialize."""
        #self._errors = {}

    async def async_step_user(self, user_input={}):
        return self.async_show_form(
            step_id='input',
            data_schema=STEP_SCHEMA
        )

    async def async_step_input(self, user_input={}):
        title = "Shelly"
        if user_input and 'id_prefix' in user_input:
            title = user_input["id_prefix"] 
        return self.async_create_entry(
            title=title,
            data=user_input
        )

    async def async_step_import(self, user_input):
        """Import a config entry.
        Special type of import, we're not actually going to store any data.
        Instead, we're going to rely on the values that are in config file.
        """
        for entry in self._async_current_entries():
            if entry.source == "import":
                return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(title="configuration.yaml",
                                       data=user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return ShellyOptionsFlowHandler(config_entry)

class ShellyOptionsFlowHandler(config_entries.OptionsFlow):
    """Shelly config flow options handler."""

    def __init__(self, config_entry):
        """Initialize Shelly options flow."""
        self.config_entry = config_entry
        self._options = {}

        if config_entry.options.get(CONF_LOCAL_PY_SHELLY):
            self._options[CONF_LOCAL_PY_SHELLY] = True

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return self.async_external_step(step_id="init", url="/shelly/config")
        
        return await self.async_step_user(user_input)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self.instance = self.hass.data[DOMAIN].instances[self.config_entry.entry_id]

        if self.instance.config_entry.source == "import" \
            and not self.instance.config_entry.options:
            return await self.async_step_yaml()

        return await self.async_step_config_1()

    def v(self, id):
        default = self.instance.conf.get(id, "")
        return vol.Optional(id, default=default)

    async def async_step_yaml(self, user_input=None):
        if not user_input:
            schema = vol.Schema({
                vol.Optional("convert", default=False): bool
            })
            return self.async_show_form(step_id="yaml", data_schema=schema)

        system_options = {}
        if user_input["convert"]:
            system_options = self.instance.conf
            data = {}
            data[CONF_OBJECT_ID_PREFIX] = \
                system_options.get(CONF_OBJECT_ID_PREFIX, "shelly")
            self.instance.hass.config_entries.async_update_entry(
                self.config_entry, data=data
            )

        return self.async_create_entry(
            title="Shelly smart home",
            data=system_options
        )

    async def async_step_config_1(self, user_input=None):
        if not user_input:
            schema = vol.Schema({
                self.v(CONF_MDNS): bool,
                self.v(CONF_VERSION): bool,
                self.v(CONF_UPGRADE_SWITCH): bool,
                self.v(CONF_UPGRADE_BETA_SWITCH): bool,
                self.v(CONF_IGMPFIX): bool,
                self.v(CONF_HOST_IP) : str,
                self.v(CONF_MQTT_PORT) : cv.positive_int
            })
            return self.async_show_form(step_id="config_1", data_schema=schema)

        self._options.update(user_input)

        return await self.async_step_config_2()

    async def async_step_config_2(self, user_input=None):
        if not user_input:
            schema = vol.Schema({
                self.v(CONF_ADDITIONAL_INFO): bool,
                self.v(CONF_SCAN_INTERVAL): int,
                self.v(CONF_UNAVALABLE_AFTER_SEC): int,
                self.v(CONF_CLOUD_AUTH_KEY) : str,
                self.v(CONF_CLOUD_SERVER) : str,
                self.v(CONF_TMPL_NAME) : str,
                self.v(CONF_USERNAME): str,
                self.v(CONF_PASSWORD): str
            })
            return self.async_show_form(step_id="config_2", data_schema=schema)

        self._options.update(user_input)

        return await self.async_step_config_mqtt()

    async def async_step_config_mqtt(self, user_input=None):
        if not user_input:
            schema = vol.Schema({
                self.v(CONF_MQTT_SERVER_HOST): str,
                self.v(CONF_MQTT_SERVER_PORT): int,
                self.v(CONF_MQTT_SERVER_USERNAME): str,
                self.v(CONF_MQTT_SERVER_PASSWORD): str,
            })
            return self.async_show_form(step_id="config_mqtt", data_schema=schema)

        self._options.update(user_input)

        return await self.async_step_attributes()


    async def async_step_attributes(self, user_input=None):

        if not user_input:
            attribs = {}
            for attrib in list(ALL_ATTRIBUTES):
                default = attrib in self.instance.conf[CONF_ATTRIBUTES]
                attribs[vol.Optional(attrib, default=default)] = bool

            return self.async_show_form(
                step_id="attributes",
                data_schema=vol.Schema(attribs)
            )

        attribs = self._options.get("attributes", [])
        for attr, value in user_input.items():
            if value:
                attribs.append(attr)

        self._options["attributes"] = attribs

        return await self.async_step_sensors()

    async def async_step_sensors(self, user_input=None):

        if not user_input:
            sensors = {}
            for sensor in list(ALL_SENSORS):
                default = sensor in self.instance.conf[CONF_SENSORS]
                sensors[vol.Optional(sensor, default=default)] = bool

            return self.async_show_form(
                step_id="sensors",
                data_schema=vol.Schema(sensors))

        sensors = self._options.get("sensors", [])
        for sensor, value in user_input.items():
            if value:
                sensors.append(sensor)

        self._options["sensors"] = sensors

        return await self.async_step_final()

    async def async_step_final(self):
        return self.async_create_entry(
            title="Shelly smart home",
            data=self._options
        )

