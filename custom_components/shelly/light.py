"""
Shelly platform for the light component.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""
import logging

from homeassistant.components.light import (
    ATTR_BRIGHTNESS, ATTR_COLOR_TEMP, ATTR_EFFECT, ATTR_HS_COLOR, 
    ATTR_WHITE_VALUE,
    SUPPORT_BRIGHTNESS, SUPPORT_COLOR, SUPPORT_COLOR_TEMP, SUPPORT_EFFECT,
    SUPPORT_WHITE_VALUE,
    Light
)
from homeassistant.helpers.dispatcher import async_dispatcher_connect
import homeassistant.util.color as color_util
from homeassistant.util.color import (
    color_temperature_kelvin_to_mired as kelvin_to_mired,
    color_temperature_mired_to_kelvin as mired_to_kelvin)

from . import ShellyDevice

_LOGGER = logging.getLogger(__name__)

SUPPORT_SHELLYRGB_COLOR = (SUPPORT_BRIGHTNESS | SUPPORT_COLOR)
SUPPORT_SHELLYRGB_WHITE = (SUPPORT_BRIGHTNESS)

# def setup_platform(hass, _config, add_devices, discovery_info=None):
#     """Setup Shelly Light platform."""
#     dev = get_device_from_hass(hass, discovery_info)
#     if dev.device_type == "RELAY":
#         add_devices([ShellyLight(dev, hass)])
#     elif dev.device_type == "DIMMER":
#         add_devices([ShellyDimmer(dev, hass)])
#     else:
#         add_devices([ShellyRGB(dev, hass)])

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Shelly light sensors dynamically."""
    async def async_discover_light(dev, instance):
        """Discover and add a discovered sensor."""
        if dev.device_type == "RELAY":
            async_add_entities([ShellyLight(dev, instance)])
        elif dev.device_type == "DIMMER":
            async_add_entities([ShellyDimmer(dev, instance)])
        else:
            async_add_entities([ShellyRGB(dev, instance)])

    async_dispatcher_connect(
        hass,
        "shelly_new_light",
        async_discover_light
    )

class ShellyLight(ShellyDevice, Light):
    """Representation of an Shelly Switch."""

    def __init__(self, dev, instance):
        """Initialize an ShellyLight."""
        ShellyDevice.__init__(self, dev, instance)
        self._state = None
        self.update()

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        self._dev.turn_on()

    def turn_off(self, **kwargs):
        self._dev.turn_off()

    def update(self):
        """Fetch new state data for this light."""
        self._state = self._dev.state

class ShellyDimmer(ShellyDevice, Light):
    """Representation of an Shelly Dimmer."""

    def __init__(self, dev, instance):
        """Initialize an ShellyDimmer."""
        ShellyDevice.__init__(self, dev, instance)
        self._state = None
        self._brightness = None
        self.update()

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        brightness = None
        if ATTR_BRIGHTNESS in kwargs:
            brightness = int(kwargs[ATTR_BRIGHTNESS] / 2.55)
        self._dev.turn_on(brightness)

    def turn_off(self, **_kwargs):
        self._dev.turn_off()

    @property
    def brightness(self):
        """Return the brightness of the light."""
        return int(self._brightness * 2.55)

    def update(self):
        """Fetch new state data for this light."""
        self._state = self._dev.state
        self._brightness = self._dev.brightness

class ShellyRGB(ShellyDevice, Light):
    """Representation of an Shelly Light."""

    def __init__(self, dev, instance):
        """Initialize an ShellyLight."""
        ShellyDevice.__init__(self, dev, instance)
        self._state = None
        self._brightness = None
        self._white_value = None
        self._rgb = None
        self._mode = None
        self._temp = None
        self._effect = None
        self.update()

    @property
    def supported_features(self):
        """Flag supported features."""
        features = SUPPORT_SHELLYRGB_WHITE \
            if self._mode == 'white' else SUPPORT_SHELLYRGB_COLOR
        if self._dev.support_color_temp and self._mode == "white":
            features = features | SUPPORT_COLOR_TEMP
        if self._dev.effects_list is not None:
            features = features | SUPPORT_EFFECT
        if self._dev.support_white_value:
            features = features | SUPPORT_WHITE_VALUE
        return features

    @property
    def effect_list(self):
        """Return the list of supported effects."""
        return list(map(lambda e: e['name'], self._dev.effects_list))

    @property
    def brightness(self):
        """Return the brightness of the light."""
        return int(self._brightness * 2.55)

    @property
    def white_value(self):
        """Return the white value of this light between 0..255."""
        return int(self._white_value)

    @property
    def is_on(self):
        """Return status of light"""
        return self._state

    def turn_on(self, **kwargs):
        """Turn on light"""
        brightness = None
        rgb = None
        temp = None
        effect_nr = None
        mode = None
        white_value = None

        if ATTR_BRIGHTNESS in kwargs:
            brightness = int(kwargs[ATTR_BRIGHTNESS] / 2.55)

        if ATTR_WHITE_VALUE in kwargs:
            white_value = int(kwargs[ATTR_WHITE_VALUE])

        if ATTR_HS_COLOR in kwargs:
            red, green, blue = \
                color_util.color_hs_to_RGB(*kwargs[ATTR_HS_COLOR])
            rgb = [red, green, blue]

        if ATTR_COLOR_TEMP in kwargs:
            temp = int(mired_to_kelvin(kwargs[ATTR_COLOR_TEMP]))

        if ATTR_EFFECT in kwargs:
            affect_attr = kwargs.get(ATTR_EFFECT)
            effect = [e for e in self._dev.effects_list
                        if e['name'] == affect_attr][0]

            #if 'mode' in effect:
            #    mode = effect['mode']

            if 'effect' in effect:
                effect_nr = effect['effect']

        self._dev.turn_on(brightness=brightness, rgb=rgb, temp=temp, mode=mode,
                          effect=effect_nr, white_value=white_value)

    def turn_off(self, **_kwargs):
        """Turn off light"""
        self._dev.turn_off()

    def update(self):
        """Fetch new state data for this light."""
        self._state = self._dev.state
        self._rgb = self._dev.rgb
        self._brightness = self._dev.brightness
        self._white_value = self._dev.white_value
        self._temp = self._dev.temp
        self._effect = self._dev.effect
        self._mode = self._dev.mode

    @property
    def hs_color(self):
        """Return the hue and saturation color value [float, float]."""
        return color_util.color_RGB_to_hs(*self._rgb)

    @property
    def color_temp(self):
        """Return the CT color value in mireds."""
        if self._temp is None:
            return None
        return int(kelvin_to_mired(self._temp))

    @property
    def min_mireds(self):
        """Return the coldest color_temp that this light supports."""
        return kelvin_to_mired(6500)

    @property
    def max_mireds(self):
        """Return the warmest color_temp that this light supports."""
        return kelvin_to_mired(3000)

    @property
    def effect(self):
        for effect in self._dev.effects_list:
            if effect['effect'] == self._effect:
                return effect['name']
        return None
