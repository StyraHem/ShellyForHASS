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
)
try:
    from homeassistant.components.light import (LightEntity)
except:
    from homeassistant.components.light import (Light as LightEntity)
from homeassistant.helpers.dispatcher import async_dispatcher_connect
import homeassistant.util.color as color_util
from homeassistant.util.color import (
    color_temperature_kelvin_to_mired as kelvin_to_mired,
    color_temperature_mired_to_kelvin as mired_to_kelvin)

from .device import ShellyDevice

_LOGGER = logging.getLogger(__name__)

SUPPORT_SHELLYRGB_COLOR = (SUPPORT_BRIGHTNESS | SUPPORT_COLOR)
SUPPORT_SHELLYRGB_WHITE = (SUPPORT_BRIGHTNESS)

# def setup_platform(hass, _config, add_devices, discovery_info=None):
#     """Setup Shelly Light platform."""
#     dev = get_device_from_hass(hass, discovery_info)
#     if dev.device_type == "RELAY":
#         add_devices([ShellyLightRelay(dev, hass)])
#     elif dev.device_type == "DIMMER":
#         add_devices([ShellyDimmer(dev, hass)])
#     else:
#         add_devices([ShellyRGB(dev, hass)])

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Shelly light sensors dynamically."""
    async def async_discover_light(dev, instance):
        """Discover and add a discovered sensor."""
        if dev.device_type == "RELAY":
            async_add_entities([ShellyLightRelay(dev, instance)])
        elif dev.device_type == "DIMMER":
            async_add_entities([ShellyDimmer(dev, instance)])
        elif dev.device_type == "RGBLIGHT":
            async_add_entities([ShellyRGB(dev, instance)])
        else:
            async_add_entities([ShellyDimmer(dev, instance)])

    async_dispatcher_connect(
        hass,
        "shelly_new_light",
        async_discover_light
    )

class ShellyLightRelay(ShellyDevice, LightEntity):
    """Representation of an Shelly Switch."""

    def __init__(self, dev, instance):
        """Initialize an ShellyLightRelay."""
        ShellyDevice.__init__(self, dev, instance)
        self._state = None
        self._master_unit = True
        self.update()

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        self._dev.turn_on()
        self._state = True
        self.schedule_update_ha_state()


    def turn_off(self, **kwargs):
        self._dev.turn_off()
        self._state = False
        self.schedule_update_ha_state()

    def update(self):
        """Fetch new state data for this light."""
        self._state = self._dev.state

class ShellyDimmer(ShellyDevice, LightEntity):
    """Representation of an Shelly Dimmer."""

    def __init__(self, dev, instance):
        """Initialize an ShellyDimmer."""
        ShellyDevice.__init__(self, dev, instance)
        self._state = None
        self._brightness = None
        self._color_temp = None
        self._color_temp_min = None
        self._color_temp_max = None
        self._master_unit = True
        self.update()

        self._features = SUPPORT_BRIGHTNESS
        if getattr(dev, "support_color_temp", False):
            self._color_temp_min = dev._color_temp_min
            self._color_temp_max = dev._color_temp_max
            self._features |= SUPPORT_COLOR_TEMP

    @property
    def supported_features(self):
        """Flag supported features."""
        return self._features

    @property
    def is_on(self):
        return self._state

    def turn_on(self, **kwargs):
        brightness = None
        color_temp = None
        if ATTR_BRIGHTNESS in kwargs:
            brightness = int(kwargs[ATTR_BRIGHTNESS] / 2.55)
            self._brightness = brightness
        if ATTR_COLOR_TEMP in kwargs:
            color_temp = int(mired_to_kelvin(kwargs[ATTR_COLOR_TEMP]))
            if color_temp > self._color_temp_max:
                color_temp = self._color_temp_max
            if color_temp < self._color_temp_min:
                color_temp = self._color_temp_min
            self._color_temp = color_temp
        if color_temp:
            self._dev.turn_on(brightness, color_temp)
        else:
            self._dev.turn_on(brightness)
        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **_kwargs):
        self._dev.turn_off()
        self._state = False
        self.schedule_update_ha_state()

    @property
    def brightness(self):
        """Return the brightness of the light."""
        return int(self._brightness * 2.55)

    @property
    def color_temp(self):
        """Return the CT color value in mireds."""
        if not self._color_temp:
            return None
        return int(kelvin_to_mired(self._color_temp))

    @property
    def min_mireds(self):
        """Return the coldest color_temp that this light supports."""
        if not self._color_temp_max:
            return None
        return kelvin_to_mired(self._color_temp_max)

    @property
    def max_mireds(self):
        """Return the warmest color_temp that this light supports."""
        if not self._color_temp_min:
            return None
        return kelvin_to_mired(self._color_temp_min)

    def update(self):
        """Fetch new state data for this light."""
        self._state = self._dev.state
        self._brightness = self._dev.brightness
        if hasattr(self._dev, 'color_temp'):
            self._color_temp = self._dev.color_temp

class ShellyRGB(ShellyDevice, LightEntity):
    """Representation of an Shelly Light."""

    def __init__(self, dev, instance):
        """Initialize an ShellyLightRelay."""
        ShellyDevice.__init__(self, dev, instance)
        self._state = None
        self._brightness = None
        self._white_value = None
        self._rgb = None
        self._mode = None
        self._color_temp = None
        self._effect = None
        self._master_unit = True
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
        color_temp = None
        effect_nr = None
        mode = None
        white_value = None

        if ATTR_BRIGHTNESS in kwargs:
            brightness = int(kwargs[ATTR_BRIGHTNESS] / 2.55)
            self._brightness = brightness

        if ATTR_WHITE_VALUE in kwargs:
            white_value = int(kwargs[ATTR_WHITE_VALUE])
            self._white_value = white_value

        if ATTR_HS_COLOR in kwargs:
            red, green, blue = \
                color_util.color_hs_to_RGB(*kwargs[ATTR_HS_COLOR])
            rgb = [red, green, blue]
            self._rgb = rgb

        if ATTR_COLOR_TEMP in kwargs:
            color_temp = int(mired_to_kelvin(kwargs[ATTR_COLOR_TEMP]))
            if color_temp > 6500:
                color_temp = 6500
            if color_temp < 3000:
                color_temp = 3000
            self._color_temp = color_temp

        if ATTR_EFFECT in kwargs:
            affect_attr = kwargs.get(ATTR_EFFECT)
            effect = [e for e in self._dev.effects_list
                        if e['name'] == affect_attr][0]

            #if 'mode' in effect:
            #    mode = effect['mode']

            if 'effect' in effect:
                effect_nr = effect['effect']
                self._effect = effect_nr

        self._dev.turn_on(brightness=brightness, rgb=rgb, color_temp=color_temp,
                          mode=mode, effect=effect_nr, white_value=white_value)

        self._state = True
        self.schedule_update_ha_state()

    def turn_off(self, **_kwargs):
        """Turn off light"""
        self._dev.turn_off()
        self._state = False
        self.schedule_update_ha_state()

    def update(self):
        """Fetch new state data for this light."""
        self._state = self._dev.state
        self._rgb = self._dev.rgb
        self._brightness = self._dev.brightness
        self._white_value = self._dev.white_value
        self._color_temp = self._dev.color_temp
        self._effect = self._dev.effect
        self._mode = self._dev.mode

    @property
    def hs_color(self):
        """Return the hue and saturation color value [float, float]."""
        return color_util.color_RGB_to_hs(*self._rgb)

    @property
    def color_temp(self):
        """Return the CT color value in mireds."""
        if not self._color_temp:
            return None
        return int(kelvin_to_mired(self._color_temp))

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
