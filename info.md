[![buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/styrahem)

This is a plugin platform for Shelly smart home WiFi devices. The plugin communicate localy with the devices. You can also enable cloud connection, now it is only used to get the names of the devices.

{%- if selected_tag == "master" %}
## This is a development version!
This is **only** intended for test by developers!
Please not install this version!
{% endif %}

{%- if prerelease %}
## This is a beta version
Please be careful and do NOT install this on production systems. Also make sure to take a backup/snapshot before installing. Check the [change log](https://github.com/StyraHem/ShellyForHASS/releases) for more information.
{% endif %}

![List](https://raw.githubusercontent.com/StyraHem/ShellyForHASS/master/images/intro.png)

# Changes
You can find change log under [releases](https://github.com/StyraHem/ShellyForHASS/releases)

# Community and support
Please join our [Facebook group](https://www.facebook.com/groups/shellyforhass) for support and information about ShellyForHass.

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
- [Change log](https://github.com/StyraHem/ShellyForHASS/releases)
- [Wiki, FAQ](https://github.com/StyraHem/ShellyForHASS/wiki)
- [Facebook group](https://www.facebook.com/groups/shellyforhass)
