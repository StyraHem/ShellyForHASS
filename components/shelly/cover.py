"""
Shelly platform for the cover component.

For more details about this platform, please refer to the documentation
https://home-assistant.io/components/shelly/
"""
from . import ShellyDevice
from homeassistant.components.cover import (
	CoverDevice, SUPPORT_OPEN, SUPPORT_CLOSE, ATTR_POSITION)

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
		self._position = 0
		self._closed = 0
		self.update()

	def _updated(self):
		pass
		
	@property
	def should_poll(self):
		"""No polling needed."""
		return False

	@property
	def current_cover_position(self):
		"""Return the current position of the cover."""
		return self._position

	@property
	def is_closed(self):
		"""Return if the cover is closed."""
		return self._closed

	#@property
	#def is_closing(self):
	#	"""Return if the cover is closing."""
	#	return self._is_closing

	#@property
	#def is_opening(self):
	#	"""Return if the cover is opening."""
	#	return self._is_opening

	#@property
	#def device_class(self):
	#	"""Return the class of this device, from component DEVICE_CLASSES."""
	#	return self._device_class

	#@property
	#def supported_features(self):
	#	"""Flag supported features."""
	#	if self._supported_features is not None:
	#		return self._supported_features
	#	return super().supported_features

	def close_cover(self, **kwargs):
		"""Close the cover."""
		#self.schedule_update_ha_state()
		self._dev.down()

	def open_cover(self, **kwargs):
		#self.schedule_update_ha_state()
		self._dev.up()

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
		except:
			pass

