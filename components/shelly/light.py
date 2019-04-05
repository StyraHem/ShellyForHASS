"""
Shelly platform for the light component.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""
import logging

from homeassistant.components.light import (
    ATTR_BRIGHTNESS, ATTR_COLOR_TEMP, ATTR_EFFECT, ATTR_HS_COLOR,
    SUPPORT_BRIGHTNESS, SUPPORT_COLOR, SUPPORT_COLOR_TEMP, SUPPORT_EFFECT,
    Light)
import homeassistant.util.color as color_util
from homeassistant.util.color import (
    color_temperature_kelvin_to_mired as kelvin_to_mired,
    color_temperature_mired_to_kelvin as mired_to_kelvin)

from . import ShellyDevice, get_device_from_hass

_LOGGER = logging.getLogger(__name__)

EFFECT_WHITE = {'name': "White", 'mode': 'white', 'effect': 0}
EFFECT_COLOR = {'name': "Color", 'mode': 'color', 'effect': 0}
EFFECT_METEOR = {'name': "Meteor Shower", 'effect': 1}
# EFFECT_GRADUAL_C = { 'name':"Gradual Change (Color)"   , 'mode':'color', 'effect':2 }
# EFFECT_GRADUAL_W = { 'name':"Gradual Change (White)"   , 'mode':'white', 'effect':2 }
EFFECT_BREATH_C = {'name': "Breath (Color)", 'mode': 'color', 'effect': 3}
EFFECT_BREATH_W = {'name': "Breath (White)", 'mode': 'white', 'effect': 3}
EFFECT_FLASH_C = {'name': "Flash (Color)", 'mode': 'color', 'effect': 4}
EFFECT_FLASH_W = {'name': "Flash (White)", 'mode': 'white', 'effect': 4}
EFFECT_ONOFF_C = {'name': "On/Off gradual (Color)", 'mode': 'color',
                  'effect': 5}
EFFECT_ONOFF_W = {'name': "On/Off gradual (White)", 'mode': 'white',
                  'effect': 5}
EFFECT_REDGREEN = {'name': "Red/Green Change", 'effect': 6}

EFFECT_LIST = [
    EFFECT_WHITE,
    EFFECT_COLOR,
    EFFECT_METEOR,
    # EFFECT_GRADUAL_C,
    # EFFECT_GRADUAL_W,
    EFFECT_BREATH_C,
    EFFECT_BREATH_W,
    EFFECT_FLASH_C,
    EFFECT_FLASH_W,
    EFFECT_ONOFF_C,
    EFFECT_ONOFF_W,
    EFFECT_REDGREEN
]

SUPPORT_SHELLYRGB_COLOR = (SUPPORT_BRIGHTNESS | SUPPORT_COLOR)
SUPPORT_SHELLYRGB_WHITE = (SUPPORT_BRIGHTNESS)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup Shelly Light platform."""
    dev = get_device_from_hass(hass, discovery_info)
    if dev.device_type == "RELAY":
        add_devices([ShellyLight(dev, hass)])
    else:
        add_devices([ShellyRGB(dev, hass)])

class ShellyLight(ShellyDevice, Light):
    """Representation of an Shelly Switch."""

    def __init__(self, dev, hass):
        """Initialize an ShellySwitch."""
        ShellyDevice.__init__(self, dev, hass)
        self._state = None
        self.update()

    def _updated(self):
        """Receive events when the switch state changed (by mobile,
        switch etc)"""
        self.schedule_update_ha_state(True)

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


class ShellyRGB(ShellyDevice, Light):
    """Representation of an Shelly Light."""

    def __init__(self, dev, hass):
        """Initialize an ShellyLight."""
        ShellyDevice.__init__(self, dev, hass)
        self._state = None
        self._brightness = None
        self._rgb = None
        self._mode = None
        self._temp = None
        self.update()

    def _updated(self):
        """Receive events when the light state changed (by mobile,
        switch etc)"""
        if self.entity_id is not None:
            self.schedule_update_ha_state(True)

    @property
    def supported_features(self):
        """Flag supported features."""
        features = SUPPORT_SHELLYRGB_WHITE \
            if self._mode == 'white' else SUPPORT_SHELLYRGB_COLOR
        if self._dev.support_color_temp and self._mode == "white":
            features = features | SUPPORT_COLOR_TEMP
        if self._dev.support_effects:
            features = features | SUPPORT_EFFECT
        return features

    @property
    def effect_list(self):
        """Return the list of supported effects."""
        return list(map(lambda e: e['name'], EFFECT_LIST))

    @property
    def brightness(self):
        """Return the brightness of the light."""
        return int(self._brightness * 2.55)

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        brightness = None
        rgb = None
        temp = None
        effect_nr = None
        mode = None

        if ATTR_BRIGHTNESS in kwargs:
            brightness = int(kwargs[ATTR_BRIGHTNESS] / 2.55)

        if ATTR_HS_COLOR in kwargs:
            red, green, blue = \
                color_util.color_hs_to_RGB(*kwargs[ATTR_HS_COLOR])
            rgb = [red, green, blue]

        if ATTR_COLOR_TEMP in kwargs:
            temp = int(mired_to_kelvin(kwargs[ATTR_COLOR_TEMP]))

        if ATTR_EFFECT in kwargs:
            affect_attr = kwargs.get(ATTR_EFFECT)
            effect = [e for e in EFFECT_LIST if e['name'] == affect_attr][0]

            if 'mode' in effect:
                mode = effect['mode']

            if 'effect' in effect:
                effect_nr = effect['effect']

        self._dev.turn_on(brightness=brightness, rgb=rgb, temp=temp, mode=mode,
                         effect=effect_nr)

    def turn_off(self, **kwargs):
        self._dev.turn_off()

    def update(self):
        """Fetch new state data for this light."""
        self._state = self._dev.state
        self._rgb = self._dev.rgb
        self._brightness = self._dev.brightness
        self._temp = self._dev.temp
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
