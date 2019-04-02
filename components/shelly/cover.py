"""
Shelly platform for the cover component.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""
from . import ShellyDevice
from homeassistant.components.cover import (
    CoverDevice, SUPPORT_STOP, SUPPORT_OPEN, SUPPORT_CLOSE, SUPPORT_SET_POSITION,
    STATE_OPEN, STATE_CLOSED, STATE_OPENING, STATE_CLOSING)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the Shelly cover platform.""" 
    dataKey = discovery_info['dataKey']
    dev = hass.data[dataKey]
    add_devices([ShellyCover(dev, hass)])
    hass.data[dataKey]=None

class ShellyCover(ShellyDevice, CoverDevice):
    """Shelly cover device."""

    def __init__(self, dev, hass):
        """Initialize the cover."""
        ShellyDevice.__init__(self,dev,hass)
        self._position = None
        self._lastDirection = None
        self._motionState = None
        self._supportPosition = None
        self.update()

    def _updated(self):
        """Receive events when the switch state changed (by mobile, switch etc)"""
        if self.entity_id is not None:
            state = self._hass.states.get(self.entity_id)
            if state is not None:
                self.update()
                self._hass.states.set(self.entity_id, self.state, state.attributes)
         
    @property
    def should_poll(self):
        """No polling needed."""
        return True

    @property
    def current_cover_position(self):
        """Return the current position of the cover."""
        return self._position

    @property
    def is_closed(self):
        if self._supportPosition==True:
            return self._position==0
        elif self._lastDirection == "close":
            return True
        elif self._lastDirection == "open":
            return False
        
    @property
    def is_closing(self):
       """Return if the cover is closing."""
       return self._motionState=="close"

    @property
    def is_opening(self):
       """Return if the cover is opening."""
       return self._motionState=="open"

    #@property
    #def device_class(self):
    #   """Return the class of this device, from component DEVICE_CLASSES."""
    #   return self._device_class
    
    @property
    def current_cover_position(self):
        if self._supportPosition==True:
            return self._position
        else:
            return None
        
    @property
    def supported_features(self):
       """Flag supported features."""
       supported_features = SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_STOP
       if self._supportPosition==True:
           supported_features |= SUPPORT_SET_POSITION
       return supported_features

    def close_cover(self, **kwargs):
        """Close the cover."""
        self._dev.up()

    def open_cover(self, **kwargs):
        """Open the cover."""
        self._dev.down()

    def set_cover_position(self, **kwargs):
        """Move the cover to a specific position."""
        pass
        
    def stop_cover(self, **kwargs):
        """Stop the cover."""
        self._dev.stop()
        
    def update(self):
        """Fetch new state data for this light.
        This is the only method that should fetch new data for Home Assistant.
        """
        try:
            self._state = self._dev.state;
            self._position = self._dev.position
            self._lastDirection = self._dev.lastDirection
            self._motionState = self._dev.motionState
            self._supportPosition = self._dev.supportPosition
        except:
            pass

