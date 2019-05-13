import logging
import netifaces
import ipaddress

def getlogger(name,path):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    fhandle = logging.FileHandler(path)
    fhandle.setLevel(logging.INFO)
    fmt = logging.Formatter(fmt="%(asctime)s  %(name)s  %(funcName)s  %(message)s")
    fhandle.setFormatter(fmt)
    logger.addHandler(fhandle)
    return logger

def get_ip():
    addresses = []
    ifaces = netifaces.interfaces()
    for iface in ifaces:
        ips = netifaces.ifaddresses(iface)
        if 2 in ips:
            ip = ipaddress.ip_address(ips[2][0]['addr'])

            if not (ip.is_loopback or ip.is_multicast or ip.is_link_local or ip.is_reserved):
                addresses.append(ip)
    return addresses