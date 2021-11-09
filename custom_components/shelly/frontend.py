"""Setup frontend for ShellyForHass."""
from homeassistant.components.http import HomeAssistantView
from aiohttp import web
import os, sys
from .ws_handler import setup_ws

class ShellyFrontend(HomeAssistantView):
    """Base View Class for Shelly."""
    requires_auth = False
    name = "shelly_files"
    url = r"/shelly_files/{requested_file:.+}"

    async def get(self, request, requested_file):  # pylint: disable=unused-argument
        """Handle Shelly Web requests."""
        #return web.Response(status=404)
        #if os.path.exists(servefile):
        path = os.path.dirname(__file__)
        #return web.FileResponse(f"{path}/www/main.js")
        #print(requested_file)
        return web.FileResponse(f"{path}/www/" + requested_file)

async def setup_frontend(instance):
    """Configure the frontend elements."""
    #from .ws_api_handlers import setup_ws_api

    instance.hass.http.register_view(ShellyFrontend())

    # Add to sidepanel
    custom_panel_config = {
        "name": "shelly4hass-frontend",
        "embed_iframe": False,
        "trust_external": False,
        "js_url": f"/shelly_files/bundle.js",
    }

    config = {}
    config["_panel_custom"] = custom_panel_config

    instance.hass.components.frontend.async_register_built_in_panel(
        component_name="custom",
        sidebar_title="Shelly",
        sidebar_icon="mdi:alpha-s-box",
        frontend_url_path="shelly",
        config=config,
        require_admin=True,
        update=True
    )

    await setup_ws(instance)
