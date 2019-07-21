import socket
import struct

#Proxy script that receive CoAP message and forward them to Shelly HASS plugin.
#Use this if you have Shelly devices on other sub-net or VLAN

#Require ShellyForHASS 0.0.15 or later

#Change to the ip-address of your HASS server
HASS_IP = "192.168.1.XXX"

UDP_IP = "224.0.1.187"
UDP_PORT = 5683

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', UDP_PORT))
mreq = struct.pack("4sl", socket.inet_aton(UDP_IP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
  try:
    #Receive CoAP message
    data, addr = sock.recvfrom(10240)
    #Tag and add device ip-address to message
    newdata = bytearray(b'prxy')
    newdata.extend(socket.inet_aton(addr[0]))
    newdata.extend(data)
    #Send to Shelly plugin
    sock.sendto(newdata, (HASS_IP, UDP_PORT))
  except Exception as e:
    print ('exception ' + str(e))
