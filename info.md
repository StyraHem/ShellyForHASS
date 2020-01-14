[![buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/styrahem)

This is a plugin platform for Shelly smart home WiFi devices. The plugin communicate localy with the devices. You can also enable cloud connection, now it is only used to get the names of the devices.

![List](https://raw.githubusercontent.com/StyraHem/ShellyForHASS/master/images/intro.png)

# Features
- Support all Shelly devices (temperature & humidity, switch, RGB, effects etc)
- Events for multiple clicks, double clicks etc.
- Only local communication, can work in parallel with MQTT or Shelly Cloud for mobile access
- Proxy support, if Shellies on different LAN than HASS
- Zero configuration with automatic discovery of all Shellies
- Immediate response, uses CoAP events from Shellies
- If CoAP not working in the network mDns is used to discover device and REST to poll status
- Sensors for all information (battery, power, rssi, uptime, over power/temp, device temperaure, cloud & mqtt connectivity)

## Support the development
Please support us by joining on [Patereon](https://www.patreon.com/shelly4hass) or buying us [some cups of coffee](https://www.buymeacoffee.com/styrahem).

# Links
- [Documentation](https://github.com/StyraHem/ShellyForHASS/blob/master/README.md)
- [Configuration](https://github.com/StyraHem/ShellyForHASS/blob/master/README.md#configure)
