import ipaddress
import netifaces
import socket

print(socket.gethostname())

# address = []
# ifaces = netifaces.interfaces()
# for iface in ifaces:
#     ips = netifaces.ifaddresses(iface)
#     if 2 in ips:
#         ip = ipaddress.ip_address(ips[2][0]['addr'])
#
#         if not (ip.is_loopback or ip.is_multicast or ip.is_link_local or ip.is_reserved):
#             address.append(ip)
