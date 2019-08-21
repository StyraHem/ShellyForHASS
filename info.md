{% if prerelease %}
## This is a beta version!
{% endif %}

This is a plugin platform for Shelly smart home WiFi devices. The plugin communicate localy with the devices.

![List](https://raw.githubusercontent.com/StyraHem/ShellyForHASS/master/images/intro.png)

# Features
- Support all Shelly devices (temperature & humidity, switch, RGB, effects etc)
- Events for multiple clicks, double clicks etc.
- Only local communication, can work in parallel with MQTT or Shelly Cloud for mobile access
- Proxy support, if Shellies on different LAN than HASS
- Zero configuration with automatic discovery of all Shellies
- Immediate response, uses CoAP events from Shellies
- Sensors for all information (battery, power, rssi, uptime, over power/temp, device temperaure, cloud & mqtt connectivity)

# Links
- [Documentation](https://github.com/StyraHem/ShellyForHASS/blob/master/README.md)
- [Configuration](https://github.com/StyraHem/ShellyForHASS/blob/master/README.md#configure)
