import socket
import struct

#You can test to add your ip address here (host_ip)
MY_IP = socket.INADDR_ANY
#MY_IP = socket.inet_aton("192.168.x.x")

UDP_IP = "224.0.1.187"
UDP_PORT = 5683

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', UDP_PORT))
mreq = struct.pack("=4sl", socket.inet_aton(UDP_IP), MY_IP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
  data = sock.recv(10240)

  print(data)
