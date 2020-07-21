# Shelly smart home platform for HASS and HASSIO

[![founder-wip](https://img.shields.io/badge/founder-Håkan_Åkerberg@StyraHem.se-green.svg?style=for-the-badge)](https://www.styrahem.se)
[![buy me a coffee](https://img.shields.io/badge/If%20you%20like%20it-Buy%20us%20a%20coffee-orange.svg?style=for-the-badge)](https://www.buymeacoffee.com/styrahem)

[![hacs_badge](https://img.shields.io/badge/HACS-Default-green.svg?style=for-the-badge)](https://github.com/custom-components/hacs)
![Github All Releases](https://img.shields.io/github/downloads/styrahem/shellyforhass/total.svg?label=Total%20downloads&style=for-the-badge)

![GitHub release (latest by date)](https://img.shields.io/github/v/release/StyraHem/ShellyForHass?label=Latest%20release&style=for-the-badge)
![stability-wip](https://img.shields.io/badge/stability-stable-green.svg?style=for-the-badge)
![GitHub Releases](https://img.shields.io/github/downloads/StyraHem/ShellyForHass/latest/total?label=Downloads&style=for-the-badge)

## Join Facebook group:
This Facebook group are used to anounce new releases etc. Please join it to be updated of new releases.
[https://www.facebook.com/groups/shellyforhass/](https://www.facebook.com/groups/shellyforhass/)

## Support the development
We spending lots of effort to make this plugin better and supporting new devices. Please support us by joining on [Patreon](https://www.patreon.com/shelly4hass), donate to [Paypal pool](https://www.paypal.com/pools/c/8n6AbR9sNk) or buying us [some cups of coffee](https://www.buymeacoffee.com/styrahem).

## Intro
This platform adds components for Shelly smart home devices to Home Assistant. There is no configuration needed, it will find all devices on your LAN and add them to Home Assistant. All communication with Shelly devices is local. You can use this plugin and continue to use Shelly Cloud, MQTT and Shelly app in your mobile if you want. A proxy can also be used to include Shellies on different LAN's.

![List](https://raw.githubusercontent.com/StyraHem/ShellyForHASS/master/images/intro.png)

If you have any problems please see the [troubleshooting guide](https://github.com/StyraHem/ShellyForHASS/blob/master/troubleshooting.md)

## Features

- Automatically discover all Shelly devices
- Monitor status (state, temperature, humidity, power, rssi, ip, fw, battery, uptime etc.)
- Control (turn on/off, dim, color, effects, up/down etc.)
- Sensors for most of the attributes
- Switch sensors to show status of switch button (0.0.16)
- Detection of click and multiple quick clicks by events
- Works with Shelly default settings, no extra configuration
- Runs locally, you don't have to add the device to Shelly Cloud
- Coexists with Shelly Cloud so you can continue to use Shelly Cloud and Shelly apps
- Using CoAP and REST for communication (not MQTT)
- Working with both static or dynamic ip addresses on your devices
- Using events so very fast response (no polling)
- Support restrict login with username and password (0.0.3-)
- Version sensor to show version of component and pyShelly (0.0.4)
- Device configuration (name, show switch as light) (0.0.4)
- Discovery can be turned off (0.0.4)
- Switch for firmware update trigger (use with monster-card to show a list of devices to need to be update, see examples below)
- Support proxy to allow Shelly devices in other LANs (0.0.15).
- Using mDns discovery and polling if CoAP not working (slower status updates) (0.1.5)
- Receive device names from Shelly Cloud (cloud_auth_key/cloud_server) (0.1.5)
- Add Shelly devices by IP-address if on different LAN or mDns and CoAP not working for discovery

## Devices supported

- Shelly 1
- Shelly 1 PM
- Temperature addon for Shelly 1(PM)
- Shelly 2 (relay or roller mode)
- Shelly 2.5 (relay or roller mode)
- Shelly 2LED (not verified)
- Shelly 3EM (0.1.7)
- Shelly 4
- Shelly Air (0.1.9)
- Shelly Bulb
- Shelly Button-1 (0.1.9)
- Shelly DUO (0.1.7)
- Shelly Dimmer / Dimmer SL
- Shelly Dimmer 2 (0.1.9)
- Shelly Door/Window
- Shelly Door/Window 2 (0.1.9)
- Shelly EM
- Shelly Flood
- Shelly Gas (0.1.9)
- Shelly H&T
- Shelly i3 (0.1.9)
- Shelly Plug
- Shelly Plug S
- Shelly RGBW2 (rgb or 4 channels)
- Shelly RGBWW
- Shelly Vintage (0.1.8)

## Installation

### Install with HACS (recomended)

Do you you have [HACS](https://community.home-assistant.io/t/custom-component-hacs) installed? Just search for Shelly and install it direct from HACS. HACS will keep track of updates and you can easly upgrade Shelly to latest version.

### Install manually

1. Install this platform by creating a `custom_components` folder in the same folder as your configuration.yaml, if it doesn't already exist.
2. Create another folder `shelly` in the `custom_components` folder. Copy all files from custom_components into the `shelly` folder. Do not copy files from master branch, download latest release (.zip) from [here](https://github.com/StyraHem/ShellyForHASS/releases).

## Setup

You can setup this component by using HA integration or config.yaml. Most of settings is available from integration but things like decimals, device specific configuration is only available when using config.yaml.

If you have the configuration in config.yaml you can convert it to internal setting by clicking the settings gear for the integration and follow the instructions. If you use advanced settings they will be lost. After conversion the settings in config.yaml will be ignored. To go back to config.yaml just delete the integration and restart HA.

### HA Integration

When you have installed Shelly you can add it in GUI under HA integration. Use the plus button and search for Shelly. You need to specify the prefix that is used as first part of the entity_id to avoid conflicts. Default is shelly.

When you have added Shelly to HA you can do the configuration by clicking the settings gear for this integration.

### Configure in config.yaml

When you have installed shelly and make sure it exists under `custom_components` folder it is time to configure it in Home Assistant.

It is very easy, just add `shelly:` to your `configuration.yaml`

#### Examples

##### Default with discovery and power sensors

```yaml
shelly:
```

##### Get device name from Shelly Cloud

```yaml
shelly:
  cloud_auth_key: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
  cloud_server: "shelly-XXXXX.shelly.cloud"
```
You will get the information for the keys above from [Shelly Cloud, User settings](https://my.shelly.cloud/#user_settings) and click GET KEY.

##### Without discovery - manually specify devices

```yaml
shelly:
  discovery: false
  version: true #add version sensor
  sensors:
    - all
  devices:      #devices to be added
    - id: "420FC7"
    - id: "13498B-1"   #Shelly 2, Id + Channel number
    - id: "7BD5F3"
      name: My cool plug   #set friendly name
      sensors: #overide global (all)
         - power
         - device_temp
```

##### With discovery - adjust some devices

```yaml
shelly:
  discovery: true  #add all devices (default)
  sensors: #sensors to show, can be override on each device
    - rssi
    - uptime
  devices:  #configure devices
    - id: "420FC7"
      light_switch: true  #add this switch as a light
      sensors: [ switch ] #Override the global sensor
    - id: "7BD5F3"
      name: My cool plug #set friendly name
```

##### Sensor, global and per device

```yaml
shelly:
  discovery: true  #add all devices (default)
  sensors:
    - all #show all sensors
  devices:  #configure devices
    - id: "420FC7"
      light_switch: true  #add this switch as a light
    - id: "7BD5F3"
      name: My cool plug #set friendly name
```
##### Discovery by ip

```yaml
shelly:
  discover_by_ip:
    - '192.168.5.44'
    - '192.168.32.11'
```

##### Events

```yaml
automation:
  - alias: "Shelly turn off and then on quickly, any switch"
    trigger:
      platform: event
      event_type: shelly_switch_click
      event_data:
        click_cnt: 2
        state: True
  - alias: "Shelly single click (momentary) on a specific switch"
    trigger:
      platform: event
      event_type: shelly_switch_click
      event_data:
        entity_id: sensor.shelly_shsw_1_XXXXXX_switch
        click_cnt: 2        
  - alias: "Shelly double click (momentary) on a specific switch"
    trigger:
      platform: event
      event_type: shelly_switch_click
      event_data:
        entity_id: sensor.shelly_shsw_1_XXXXXX_switch
        click_cnt: 4        
```
##### Decimal and unit settings
```yaml
shelly:
  settings:
    temperature: { decimals: 1 }
    current: { decimals:0, div:1000, unit:'mA' }  #Show current as mA
  devices:
    - id: 123456
      settings:
        total_consumption: { decimals: 3, div:1000000, unit:'MWh' }   #Show MWh for a specific device
```

#### Parameters

| Parameter              | Description                                                                                            | Default | Version |
|------------------------|--------------------------------------------------------------------------------------------------------|---------|---------|
| host_ip | Use this to listen on right interface, should be the ip address of Home Assistant | | 0.1.6- |
| username               | User name to use for restrict login                                                                    |         | 0.0.3-  |
| password               | Password to use for restrict login                                                                     |         | 0.0.3-  |
| discovery              | Enable or disable discovery                                                                            | True    | 0.0.4-  |
| version                | Add a version sensor to with version of component and pyShelly                                         | False   | 0.0.4-  |
| devices                | Config for each device, se next table for more info                                                    |         | 0.0.4-  |
| show_id_in_name        | Add Shelly Device id to the end of the name                                                            | False   | 0.0.5-  |
| id_prefix              | Change the prefix of the entity id and unique id of the device                                         | shelly  | 0.0.5-  |
| igmp_fix               | Enable sending out IP_ADD_MEMBERSHIP every minute                                                      | False   | 0.0.5-  |
| additional_information | Retrieve additional information (rssi, ssid, uptime, ..)                                               | True    | 0.0.6-  |
| scan_interval          | Update frequency for polling status and additional information. If the not CoAP supported this will be the delay for status updates. | 60      | 0.0.6-  |
| _wifi_sensor_          | Add extra sensor for wifi signal of each device. Requires `additional_information` to be `True`.  | False   | 0.0.6 (deprecated) |
| _uptime_sensor_        | Add extra sensor for device uptime of each devivce. Requires `additional_information` to be `True` | False   | 0.0.6 (deprecated)  |
| power_decimals         | Round power sensor values to the given number of decimals                                          |         | 0.0.14- |
| sensors                | A list with sensors to show for each device. See list below.                                        | current_consumption | 0.0.15- |
| attributes             | A list with attributes to show for each device. See list below.                                        | default | 0.0.16- |
| upgrade_switch         | Add firmware switches when upgrade needed.                                                           | True  | 0.0.15- |
| unavailable_after_sec  | Number of seconds before the device will be unavialable      | 60 | 0.0.16- |
| mdns | Allow the plugin to use mDns to discover devices | True | 0.1.5- |
| cloud_auth_key | Use this to allow the plugin to connect to your Shelly Cloud. You will find this information at https://my.shelly.cloud/#user_settings and GET KEY | | 0.1.5- |
| cloud_server | Use this togheter with cloud_auth_key | | 0.1.5- |
| tmpl_name | Template how to create the friendly name from Shelly Cloud | {room} - {name} | 0.1.5- |
| discover_by_ip | This is a list of ip-addresses to force the plugin to discover. Use this if not CoAP or mDns discovery working for your device. | | 0.1.5- |

#### Device configuration

| Parameter    | Description                                                                               | Example        | Version |
|--------------|-------------------------------------------------------------------------------------------|----------------|---------|
| id           | Device id, same as in mobile app                                                          | 421FC7         |         |
| name         | Specify if you want to set a name of the device                                           | My Cool Shelly |         |
| entity_id    | Override the auto generated part of entity_id, like shsw_1_500500                         | bedlamp        | 0.0.16- |
| light_switch | Show this switch as a light                                                               | True           |         |
| sensors      | A list with sensors to show for each device. This will override the global sensors. See list below.  |                | 0.0.15- |
| upgrade_switch | Add firmware switches when upgrade needed. Override global configuration.               | False    | 0.0.15- |
| unavailable_after_sec  | Overide number of seconds before the device will be unavialable.    | 120 | 0.0.16- | 

#### Attributes (0.1.6-)
| Sensor       | Description                                               | Default | Version |
|--------------|-----------------------------------------------------------|---------|---------|
| all          | Show all available attributes                             ||
| default      | Attributes with the mark in default column                ||
| ip_address   | IP address of the Shelly device                       | x |
| shelly_type  | Type of Shelly (Shelly 1, Shelly 2 etc)               | x |
| shelly_id    | Shelly id of the device, 6 or 12 digits hex number    | x |
| ssid         | SSID the device is connected to                       ||
| rssi         | WiFi quality for the device  ||
| uptime       | Total uptime (s) for device ||
| has_firmware_update | Indicate if the device have a new firmware available | x |
| latest_fw_version | The newest firmware for the device type ||
| firmware_version | Current firmware version on device ||
| cloud_enabled | Shelly cloud enabled for device ||
| cloud_connected | Device connected to the cloud ||
| cloud_status | Shelly cloud status (disabled/disconnected/connected) | x |
| mqtt_connected | Device connected to MQTT server ||
| switch       | Show state of the actual switch button | x |
| current_consumption | Show power consumtion  ||
| total_consumption | Show total power consumtion  ||
| total_returned | Show total power returned  (EM/3EM) ||0.1.7-|
| voltage | Show current voltage (V) ||0.1.7-|
| current | Show current current (A) ||0.1.7-|
| power_factor | Show current power factor ||0.1.7-|
| over_power   | Show over power sensors               | x |
| device_temp  | Show device inner temperature sensors ||
| over_temp    | Show over temperature sensors         | x |
| battery      | Show battery percentage               | x |
| payload | Show the latest CoAP message received (DEBUG) ||

#### Sensors
| Sensor       | Description                           | Values / Unit     | Version |
|--------------|---------------------------------------|-------------------|---------|
| all          | Show all available sensors            |                   |
| current_consumption | Show power consumtion sensors     | W              |
| total_consumption | Show total power consumtion sensors | Wh             |
| rssi         | Show WiFi quality sensors             | dB                |
| uptime       | Show uptime sensors                   | s                 |
| over_power   | Show over power sensors               | True, False       |
| device_temp  | Show device inner temperature sensors | °C                |
| over_temp    | Show over temperature sensors         | True, False       |
| cloud        | Show cloud status                     | disabled, disconnected, connected |
| mqtt         | Show mqtt connection state            | True, False       |
| battery      | Show battery percentage (H&T)         | %                 |
| switch       | Show state of the actual switch button| True, False       |
| total_returned | Show total power returned  (EM/3EM) ||0.1.7-|
| voltage | Show current voltage |V|0.1.7-|
| current | Show current current |A|0.1.7-|
| power_factor | Show current power factor ||0.1.7-|

All of the sensors (not current_consumption) require additional_information to be True to work.

#### Types (decimal, units) and default settings (0.1.7)
| value | unit | decimals | divider |
--------|-----|-----------|---------|
| temperature | °C | 0 |    |
| device_temp | °C | 0 |    |
| illuminance | lux | 0 |    |
| humidity | % | 0 |    |
| total_consumption | kWh | 2 |  1000 |
| total_returned | kWh | 2 |  1000  |
| current_consumption | W | 0 |    |
| current | A | 1 |    |
| humidity | % | 0 |    |
| voltage | V | 0 | |
| power_factor | | 1 |
| uptime | h | 0 | 3600 |
| rssi | dB | 0 |  |

If you disable discovery only Shellies under devices will be added.

You can only specify one username and password for restrict login. If you enter username and password, access to devices without restrict login will continue to work. Different logins to different devices will be added later.

### Events
[Events added in release 0.0.16]
#### shelly_switch_click
When the switch sensor is enabled an event will be sent for multiple clicks on the switch button. This can be used to trig automations for double clicks etc.

```json
{
    "event_type": "shelly_switch_click",
    "data": {
        "entity_id": "sensor.shelly_shsw_1_xxxxxx_switch",
        "click_cnt": 4,
        "state": true
}
```
| Parameter | Description                                                                                 |
|-----------|---------------------------------------------------------------------------------------------|
| click_cnt | Number of clicks, 2 = turn back and forth quickly, 4 = double click on momentary switch.    |
| state     | Current state of the switch, can be uset to distinct on-off-on from off-on-off for example. |

### Restart Home Assistant

Now you should restart Home Assistant to load shelly. Some times you need to restart twice to get the required library pyShelly installed. You can see this error in the log file.

Shelly will discover all devices on your LAN and show them as light, switch, sensor and cover in Home Assistant.

### Proxy for VLAN or different network
If you're running Shellies on a different VLAN or network there is a [proxy.py](https://github.com/StyraHem/ShellyForHASS/blob/master/util/proxy.py) that can be used to forward CoAP messages to ShellyForHASS plugin.

Update the script with the ip-address of your HASS installation and run it on a computer/router etc that are connected to same network as your Shellies. Firewall and routing must be enabled, TCP 80 HASS -> Shelly and UDP 5683 Shelly -> HASS. If you're using multiple network interfaces, try routing the multicast packets to the right interface (i.e. `ip route add 224.0.1.187/32 dev eth1`).

## Auto entities (before Monster card)
You can use the component with [auto entities](https://github.com/thomasloven/lovelace-auto-entities) to filter data in a nice way.

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
type: 'custom:auto-entities'
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
type: 'custom:auto-entities'
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
type: 'custom:auto-entities'
```

## Feedback

Please give us feedback on info@styrahem.se or Facebook groups: [Shelly grupp (Swedish)](https://www.facebook.com/groups/ShellySweden) or [Shelly support group (English)](https://www.facebook.com/groups/ShellyIoTCommunitySupport/)

## Founder

This plugin is created by the StyraHem.se, the Swedish distributor of Shelly. In Sweden you can buy Shellies from [StyraHem.se](https://www.styrahem.se/c/126/shelly) or any of the retailers like m.nu, Kjell&Company etc.

[![buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/styrahem)

## Thanks to
- [@tefinger](https://github.com/tefinger) that have test and add functinallity to improve this component.
- Allterco that have developed all nice Shellies and also response quickly on requests and bugfixes.

## Screenshots

![List](https://raw.githubusercontent.com/StyraHem/ShellyForHASS/master/screenshots/List.PNG)
![RGB](https://raw.githubusercontent.com/StyraHem/ShellyForHASS/master/screenshots/RGB.PNG)
![Effects](https://raw.githubusercontent.com/StyraHem/ShellyForHASS/master/screenshots/Effects.PNG)
![White](https://raw.githubusercontent.com/StyraHem/ShellyForHASS/master/screenshots/White.PNG)
