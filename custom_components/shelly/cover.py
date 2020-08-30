"""
Shelly platform for the cover component.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""

#pylint: disable=import-error
from homeassistant.components.cover import (ATTR_POSITION,
                                            SUPPORT_CLOSE,
                                            SUPPORT_OPEN, SUPPORT_STOP,
                                            SUPPORT_SET_POSITION)

try:
    from homeassistant.components.cover import CoverEntity
except:
    from homeassistant.components.cover import \
        CoverDevice as CoverEntity

from .device import ShellyDevice
from homeassistant.helpers.dispatcher import async_dispatcher_connect

#def setup_platform(hass, _config, add_devices, discovery_info=None):
#    """Set up the Shelly cover platform."""
#    dev = get_device_from_hass(hass, discovery_info)
#    add_devices([ShellyCover(dev, instance)])

async def async_setup_entry(hass, _config_entry, async_add_entities):
    """Set up Shelly cover dynamically."""
    async def async_discover_cover(dev, instance):
        """Discover and add a discovered cover."""
        async_add_entities([ShellyCover(dev, instance)])

    async_dispatcher_connect(
        hass,
        "shelly_new_cover",
        async_discover_cover
    )

class ShellyCover(ShellyDevice, CoverEntity):
    """Shelly cover device."""

    def __init__(self, dev, instance):
        """Initialize the cover."""
        ShellyDevice.__init__(self, dev, instance)
        self._position = None
        self._last_direction = None
        self._motion_state = None
        self._support_position = None
        self._state = None
        self._master_unit = True
        self.update()

    @property
    def should_poll(self):
        """No polling needed."""
        return True

    @property
    def current_cover_position(self):
        """Return current position"""
        if self._support_position:
            return self._position

        return None

    @property
    def is_closed(self):
        """Return if the cover is closed or not."""
        if self._support_position:
            return self._position == 0

        return None

    @property
    def is_closing(self):
        """Return if the cover is closing."""
        return self._motion_state == "close"

    @property
    def is_opening(self):
        """Return if the cover is opening."""
        return self._motion_state == "open"

    @property
    def supported_features(self):
        """Flag supported features."""
        supported_features = SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_STOP
        if self._support_position:
            supported_features |= SUPPORT_SET_POSITION
        return supported_features

    def close_cover(self, **_kwargs):
        """Close the cover."""
        self._dev.down()

    def open_cover(self, **_kwargs):
        """Open the cover."""
        self._dev.up()

    def set_cover_position(self, **kwargs):
        """Move the cover to a specific position."""
        pos = kwargs[ATTR_POSITION]
        self._dev.set_position(pos)
        self._position = pos
        self.schedule_update_ha_state()

    def stop_cover(self, **_kwargs):
        """Stop the cover."""
        self._dev.stop()

    def update(self):
        """Fetch new state data for this light.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self._dev.state
        self._position = self._dev.position
        self._last_direction = self._dev.last_direction
        self._motion_state = self._dev.motion_state
        self._support_position = self._dev.support_position
