from kazoo.client import KazooClient
import time
import json
import subprocess
import os


zk = KazooClient(hosts="127.0.0.1:2181, 127.0.0.1:2182, 127.0.0.1:2183")
zk.start()


try:
    zk.get("/services")
except Exception as e:
    zk.create("/services", "")
else:
    pass
finally:
    pass
    
@zk.ChildrenWatch("/services")
def watch_node(children):
    print(children)



while True:
    time.sleep(100)
    print('tick')
