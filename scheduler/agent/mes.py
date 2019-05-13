import uuid
import socket
import netifaces
import ipaddress
import os

class Message:

    def __init__(self, myidpath):
        if os.path.exists(myidpath):
            with open(myidpath) as f:
                self.id = f.readline().rstrip()
                if not self.id:
                    self.id = uuid.uuid4().hex
        else:
            self.id = uuid.uuid4().hex
            with open(myidpath,'w') as f:
                self.id = f.write(self.id)


    def get_address(self):
        addresses = []
        ifaces = netifaces.interfaces()
        for iface in ifaces:
            ips = netifaces.ifaddresses(iface)
            if 2 in ips:
                ip = ipaddress.ip_address(ips[2][0]['addr'])

                if not (ip.is_loopback or ip.is_multicast or ip.is_link_local or ip.is_reserved):
                    addresses.append(str(ip))
        return addresses

    def reg(self):
        """生成注册信息"""
        return {
            "type":"register",
            "payload":{'id':self.id,
            "hostname":socket.gethostname(),
            "ip":self.get_address()}
        }
    def heartbeat(self):
        """生成心跳信息"""
        return {
            "type": "heartbeat",
            "payload": {'id': self.id,
                        "hostname": socket.gethostname(),
                        "ip": self.get_address()}
        }

    def result(self, task_id, code ,output):
        return {
            "type": "result",
            "payload": {"id": task_id,
                        "agent_id":self.id,
                        "code":code,
                        "output": output}
        }