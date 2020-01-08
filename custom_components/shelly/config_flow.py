"""Adds config flow for HACS."""
# pylint: disable=dangerous-default-value
import logging
import voluptuous as vol
#from aiogithubapi import AIOGitHub, AIOGitHubException, AIOGitHubAuthentication
from homeassistant import config_entries
#from homeassistant.core import callback
#from homeassistant.helpers import aiohttp_client

from .const import DOMAIN
#from .configuration_schema import hacs_base_config_schema, hacs_config_option_schema


_LOGGER = logging.getLogger(__name__)


class ShellyFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for HACS."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        #self._errors = {}

    async def async_step_user(self, user_input={}):
        return self.async_show_form(
            step_id='user',
            data_schema=vol.Schema({
                vol.Required('password'): str
            })
        )

    async def async_step_import(self, user_input):
        """Import a config entry.
        Special type of import, we're not actually going to store any data.
        Instead, we're going to rely on the values that are in config file.
        """
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        return self.async_create_entry(title="configuration.yaml", data={})