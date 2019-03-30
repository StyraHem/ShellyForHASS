[![founder-wip](https://img.shields.io/badge/founder-StyraHem.se-green.svg?style=for-the-badge)](https://www.styrahem.se)

![stability-wip](https://img.shields.io/badge/stability-work_in_progress-lightgrey.svg?style=for-the-badge)
![version-wip](https://img.shields.io/badge/version-0.0.2-green.svg?style=for-the-badge)


# Shelly smart home platform for HASS
This platform adds components for Shelly smart home devices to Home Assistant. There is no configuration needed it will find all devices on your LAN and add them to Home Assistant. All communication with Shelly devices are locally. You can use this plugin and continue to use Shelly Cloud and Shelly app in your mobile if you want.

## Features
- Automatically discover all Shelly devices
- Monitor status (state, temperature, humidity, power etc.)
- Control (turn on/off, dim, color, effects, up/down etc.)
- Works with Shelly default settings, no extra configuration
- Run locally, you dont have to add the device to Shelly Cloud
- Coexist with Shelly Cloud so you can continue to use Shelly Cloud and Shelly apps
- Using CoAP and REST for communication (not MQTT)
- Working with both static or dynamic ip addresses on your devices
- Using events so very fast response (no polling)

## Devices supported
- Shelly 1
- Shelly 2 (relay or roller mode)
- Shelly 4
- Shelly PLUG
- Shelly BULB
- Shelly RGBWW
- Shelly RGBW2
- Shelly H&T
- Shelly 2LED (not tested)
- Shelly 2.5 (not tested)
- Shelly PLUG S (not tested)

## Installation

### (not working yet) Install with Custom Updater
Do you you have [Custom updater](https://github.com/custom-components/custom_updater) installed? Then you can use the service [custom_updater.install](https://github.com/custom-components/custom_updater/wiki/Services#install-element-cardcomponentpython_script) with the parameter {"element":"shelly"} to install Shelly.

### Install manually
1. Install this platform by creating a `custom_components` folder in the same folder as your configuration.yaml, if it doesn't already exist.
2. Create another folder `shelly` in the `custom_components` folder. Copy all 5 Python (.py) files into the `shelly` folder. Use `raw version` if you copy and paste the files from the browser.

## Configure
When you have installed shelly and make sure it exists under `custom_components` folder it is time to configure it in Home Assistant.

It is very easy, just add this to `config.yaml`
```
shelly:
```
(Options will be added later)

## Restart Home Assistant
Now you should restart Home Assistant to load shelly

Shelly will discover all devices on your LAN and show them as light, switch, sensor and cover in Home Assistant.

## Feedback
Please give us feedback on info@styrahem.se or Facebook groups: [Shelly grupp (Swedish)](https://www.facebook.com/groups/ShellySweden) or [Shelly support group (English)](https://www.facebook.com/groups/ShellyIoTCommunitySupport/)

## Screen shots
![](https://raw.githubusercontent.com/StyraHem/hass/master/screenshots/List.PNG)
![](https://raw.githubusercontent.com/StyraHem/hass/master/screenshots/RGB.PNG)
![](https://raw.githubusercontent.com/StyraHem/hass/master/screenshots/Effects.PNG)
![](https://raw.githubusercontent.com/StyraHem/hass/master/screenshots/White.PNG)

