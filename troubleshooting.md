# This is a guide about trouble shooting ShellyForHass

This is just a start, please help me adding more information!

## Why is my devices not discovered?
The plugin trying to discover Shelly devices by listening for CoAP and mDns messages on the network.

### CoAP
CoAP is a multicast all Shelly send on the network used for discovery and and status updates.
Protocol: multicast UDP 224.0.1.187 port 5683

For this to work your router and switches must forward this to the Home Assistant server. The plugin tell routers and switches that it want to recevice this bradcast by sending a IP_MEMBER_ADD request on startup. If you enable the flag igmp_fix it will send this repeatly every minute.

If this is not working and the status updates will be slow. You can try to change IGMP setting in your router/switch to enable this.

#### CoAP and [ASUS AiMesh](https://www.asus.com/aimesh)

CoAP doesn't seem to work between AiMesh-nodes. Make sure both Home Assistant and all your Shelly-devices are connected to the main AiMesh-router. If you have Shelly-devices that are out of range from your AiMesh-router, they will not be able to push real-time updates via CoAP.

For your Shelly-devices that are in range of the AiMesh-router, you can disable roaming by adding them to the Roaming Block List:
1. Turn off all your AiMesh-nodes and let all your Shelly-devices connect to the main AiMesh-router.
2. Go to your router's admin-panel and navigate to **Advanced Settings** > **Wireless** > **Roaming Block List**.
3. Add the MAC-addresses to your Shelly-devices to the block list (you'll find them in the dropdown-list) and click **Apply**.
4. Turn your AiMesh-nodes back on. Your Shellies will now stay connected to the AiMesh-router and, if you're not suffering from other network-related problems, CoAP-discovery and CoAP-msg will now function as expected.

### mDns
mDns is a multicast every Shelly sending to anounce there ip-address. The plugin using them to discover the devices.
Protocol: multicast UDP 224.0.0.251 port 5353

Most routers and switchis forward mDns messages by default. The mDns does not have any status information so the plugin will poll the Shelly device to get status. Default poll interval is 60 sec but can be changed to around 5 sec to get faster updates. You change this by the scan_interval setting.

### Discover by ip
If none of CoAP or mDns working you can specify the ip by using the discover_by_ip setting.
