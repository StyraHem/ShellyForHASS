# This is a guide about trouble shooting ShellyForHass

This is just a start, please help me adding more information!

## Why is my devices not discovered?
The plugin trying to discover Shelly devices by listening for CoAP and mDns messages on the network.

### CoAP
CoAP is a multicast all Shelly send on the network used for discovery and and status updates.
Protocol: multicast UDP 224.0.1.187 port 5683

For this to work your router and switches must forward this to the Home Assistant server. The plugin tell routers and switches that it want to recevice this bradcast by sending a IP_MEMBER_ADD request on startup. If you enable the flag igmp_fix it will send this repeatly every minute.

If this is not working and the status updates will be slow. You can try to change IGMP setting in your router/switch to enable this.

### mDns
mDns is a multicast every Shelly sending to anounce there ip-address. The plugin using them to discover the devices.
Protocol: multicast UDP 224.0.0.251 port 5353

Most routers and switchis forward mDns messages by default. The mDns does not have any status information so the plugin will poll the Shelly device to get status. Default poll interval is 60 sec but can be changed to around 5 sec to get faster updates. You change this by the scan_interval setting.

### Discover by ip
If none of CoAP or mDns working you can specify the ip by using the discover_by_ip setting.
