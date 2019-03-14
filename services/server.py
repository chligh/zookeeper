from kazoo.client import KazooClient
import time
import json
import subprocess
import os


zk = KazooClient(hosts="127.0.0.1:2181, 127.0.0.1:2182, 127.0.0.1:2183")
zk.start()


def getip(ifname = 'eth0'):

    import socket, fcntl, struct  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))  
    ret = socket.inet_ntoa(inet[20:24])  
    return ret  


try:
    zk.get("/services")
except Exception as e:
    zk.create("/services", "")
else:
    pass
finally:
    pass
    
ip=getip()

znode = {"ip": ip} 
znode = json.dumps(znode)
znode = bytes(znode)
zk.create("/services/svr", znode, ephemeral=True, sequence=True)




while True:
    time.sleep(100)
    print('tick')
