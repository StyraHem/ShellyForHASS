# Shelly smart home platform for HASS

[![founder-wip](https://img.shields.io/badge/founder-Håkan_Åkerberg@StyraHem.se-green.svg?style=for-the-badge)](https://www.styrahem.se)
[![buy me a coffee](https://img.shields.io/badge/If%20you%20like%20it-Buy%20me%20a%20coffee-orange.svg?style=for-the-badge)](https://www.buymeacoffee.com/styrahem)

![stability-wip](https://img.shields.io/badge/stability-stable-green.svg?style=for-the-badge)
![version-wip](https://img.shields.io/badge/version-0.0.14-green.svg?style=for-the-badge)

This platform adds components for Shelly smart home devices to Home Assistant. There is no configuration needed, it will find all devices on your LAN and add them to Home Assistant. All communication with Shelly devices are locally. You can use this plugin and continue to use Shelly Cloud, MQTT and Shelly app in your mobile if you want.

## Features

- Automatically discover all Shelly devices
- Monitor status (state, temperature, humidity, power, rssi, ip, fw, battery, uptime etc.)
- Control (turn on/off, dim, color, effects, up/down etc.)
- Works with Shelly default settings, no extra configuration
- Run locally, you don't have to add the device to Shelly Cloud
- Coexist with Shelly Cloud so you can continue to use Shelly Cloud and Shelly apps
- Using CoAP and REST for communication (not MQTT)
- Working with both static or dynamic ip addresses on your devices
- Using events so very fast response (no polling)
- Support restric login with username and password (0.0.3-)
- Version sensor to show version of component and pyShelly (0.0.4)
- Device configuration (name, show switch as light) (0.0.4)
- Discovery can be turned off (0.0.4)
- Switch for firmware update trigger (use with monster-card to show a list of devices to need to be update, see examples below)

## Devices supported

- Shelly 1
- Shelly 1 PM (no power meter, firmware bug)
- Shelly 2 (relay or roller mode)
- Shelly 2.5 (relay or roller mode)
- Shelly 4
- Shelly PLUG
- Shelly BULB
- Shelly RGBWW
- Shelly RGBW2
- Shelly H&T
- Shelly 2LED (not tested)
- Shelly PLUG S (not tested)

## Installation

### Install with Custom Updater

Do you you have [Custom updater](https://github.com/custom-components/custom_updater) installed? Then you can use the service [custom_updater.install](https://github.com/custom-components/custom_updater/wiki/Services#install-element-cardcomponentpython_script) with the parameter {"element":"shelly"} to install Shelly.

Custom updater also let you to upgrade to latest version. We recomend you to use this.

### Install manually

1. Install this platform by creating a `custom_components` folder in the same folder as your configuration.yaml, if it doesn't already exist.
2. Create another folder `shelly` in the `custom_components` folder. Copy all 5 Python (.py) files into the `shelly` folder. Use `raw version` if you copy and paste the files from the browser.

## Configure

When you have installed shelly and make sure it exists under `custom_components` folder it is time to configure it in Home Assistant.

It is very easy, just add `shelly` this to your `configuration.yaml`

### Examples

```yaml
shelly:
```

#### Without discovery - manually specify devices

```yaml
shelly:
  discovery: false
  version: true #add version sensor
  devices:      #devices to be added
    - id: 420FC7
    - id: 13498B-1   #Shelly 2, Id + Channel number
    - id: 7BD5F3
      name: My cool plug   #set friendly name
```

#### With discovery - adjust some devices

```yaml
shelly:
  discovery: true  #add all devices (default)
  devices:  #configure devices
    - id: 420FC7
      light_switch: true  #add this switch as a light
    - id: 7BD5F3
      name: My cool plug #set friendly name
```

### Parameters

| Parameter              | Description                                                                                            | Default | Version |
|------------------------|--------------------------------------------------------------------------------------------------------|---------|---------|
| username               | User name to use for restrict login                                                                    |         | 0.0.3-  |
| password               | Password to use for restrict login                                                                     |         | 0.0.3-  |
| discovery              | Enable or disable discovery                                                                            | True    | 0.0.4-  |
| version                | Add a version sensor to with version of component and pyShelly                                         | False   | 0.0.4-  |
| devices                | Config for each device, se next table for more info                                                    |         | 0.0.4-  |
| show_id_in_name        | Add Shelly Device id to the end of the name                                                            | False   | 0.0.5-  |
| id_prefix              | Shange the prefix of the entity id and unique id of the device                                         | shelly  | 0.0.5-  |
| igmp_fix               | Enable sending out IP_ADD_MEMBERSHIP every minute                                                      | False   | 0.0.5-  |
| additional_information | Retrieve additional information (rssi, ssid, uptime, ..)                                               | True    | 0.0.6-  |
| scan_interval          | Update frequency for additional information                                                            | 60      | 0.0.6-  |
| wifi_sensor            | Add extra sensor for wifi signal of each device. Requires `additional_information` to be `True`    | False   | 0.0.6-  |
| uptime_sensor          | Add extra sensor for device uptime of each devivce. Requires `additional_information` to be `True` | False   | 0.0.6-  |
| power_decimals         | Round power sensor values to the given number of decimals                                          |         | 0.0.14- |

#### Device configuration

| Parameter    | Description                                     | Example        |
|--------------|-------------------------------------------------|----------------|
| id           | Device id, same as in mobile app                | 421FC7         |
| name         | Specify if you want to set a name of the device | My Cool Shelly |
| light_switch | Show this switch as a light                     | True           |

If you disable discovery only Shellies under devices will be added.

You can only specify one username and password for restrict login. If you enter username and password, access to devices without restrict login will continue to work. Different logins to different deveces will be added later.

### Restart Home Assistant

Now you should restart Home Assistant to load shelly. Some times you need to restart twice to get the required library pyShelly installed. You can see this error in the log file.

Shelly will discover all devices on your LAN and show them as light, switch, sensor and cover in Home Assistant.

## Monster card
You can use the component with [monstercard](https://github.com/ciotlosm/custom-lovelace/tree/master/monster-card) to present data in a nice way.

### All shelly devices
```yaml
card:
  show_header_toggle: false
  title: Shelly
  type: entities
filter:
  exclude:
    - entity_id: '*rssi*'
    - entity_id: '*uptime*'
    - entity_id: '*firmware*'
  include:
    - entity_id: '*shelly*'
type: 'custom:monster-card'
```

### Need firmware update (click on the switch to update)
```yaml
card:
  show_header_toggle: false
  title: Shelly need update
  type: entities
filter:
  include:
    - entity_id: '*firmware_update*'
type: 'custom:monster-card'
```

### WiFi signal of all devices (rssi)
```yaml
card:
  show_header_toggle: false
  title: Shelly
  type: entities
filter:
  include:
    - entity_id: '*rssi*'
type: 'custom:monster-card'
```

## Feedback

Please give us feedback on info@styrahem.se or Facebook groups: [Shelly grupp (Swedish)](https://www.facebook.com/groups/ShellySweden) or [Shelly support group (English)](https://www.facebook.com/groups/ShellyIoTCommunitySupport/)

## Founder

This plugin is created by the StyraHem.se, the Swedish distributor of Shelly. In Sweden you can buy Shellies from [StyraHem.se](https://www.styrahem.se/c/126/shelly) or any of the retailers like Kjell&Company.

[![buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/styrahem)

## Screen shots

![List](https://raw.githubusercontent.com/StyraHem/hass/master/screenshots/List.PNG)
![RGB](https://raw.githubusercontent.com/StyraHem/hass/master/screenshots/RGB.PNG)
![Effects](https://raw.githubusercontent.com/StyraHem/hass/master/screenshots/Effects.PNG)
![White](https://raw.githubusercontent.com/StyraHem/hass/master/screenshots/White.PNG)
