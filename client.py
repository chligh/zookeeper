from kazoo.client import KazooClient
import time
import json
import subprocess
import os


zk = KazooClient(hosts="127.0.0.1:2181, 127.0.0.1:2182, 127.0.0.1:2183")
zk.start()



def handle_watch(data):
    try:
        info = json.loads(data)
        if not isinstance(info, dict):
            raise Exception("not json format")
        if not "ip" in info:
            raise Exception("[ip] missing in json")
        if not "commitId" in info:
            raise Exception("[commitId] missing in json")

        print("ip:" + info["ip"] + ",commitId:" + info["commitId"])

    except Exception as e:
        print(e)
        print("update fail")
        return 1
    else:
        print("update success")
        return 0
    finally:
        pass


@zk.DataWatch("/app_version")
def watch_node(data, stat):
    if data:
        data = data.decode("utf-8")
        handle_watch(data)
    else:
        print("Data is empty!")

znode = {"url": "https://github.com/chligh/zookeeper.git","path": "/tmp/zookeeper_git"}
znode = json.dumps(znode)
znode = bytes(znode)

try:
    zk.get("/app_config")
except Exception as e:
    zk.create("/app_config", znode)
else:
    zk.set("/app_config", znode)
finally:
    pass


while True:
    time.sleep(100)
    print('tick')
