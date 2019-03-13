from kazoo.client import KazooClient
import time
import json
import subprocess
import os


zk = KazooClient(hosts="127.0.0.1:2181, 127.0.0.1:2182, 127.0.0.1:2183")
zk.start()



def go_dir(dir_name):
    if os.path.exists(dir_name):
        pass
    else:
        os.makedirs(dir_name)
    os.chdir(dir_name)

def getip(ifname = 'eth0'):

    import socket, fcntl, struct  
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))  
    ret = socket.inet_ntoa(inet[20:24])  
    return ret  


def handle_watch(data):
    try:
        info = json.loads(data)
        if not isinstance(info, dict):
            raise Exception("not json format")
        if not "path" in info:
            raise Exception("[path] missing in json")
        if not "url" in info:
            raise Exception("[url] missing in json")

        chdir = info["path"]
        go_dir(chdir)

        res = subprocess.call(['git', 'status'])
        if 0 == res:
            res = subprocess.call(['git', 'pull'])
        else:
            res = subprocess.call(['git', 'clone', info["url"], '.'])

        if 0 != res:
            raise Exception("clone/pull error")

        

    except Exception as e:
        print(e)
        print("update fail")
        return 1
    else:
        print("update success")
       
    finally:
        pass

    commitId = subprocess.check_output(["git", "rev-parse", "HEAD"])
    commitId = commitId.decode()
    commitId = commitId.strip()

    ip=getip()

    znode = {"ip": ip, "commitId":commitId} 
    znode = json.dumps(znode)
    znode = bytes(znode)
    print(znode)
    
    try:
        zk.get("/app_version")
    except Exception as e:
        zk.create("/app_version", znode)
    else:
        zk.set("/app_version", znode)
    finally:
        pass


@zk.DataWatch("/app_config")
def watch_node(data, stat):
    if data:
        data = data.decode("utf-8")
        handle_watch(data)
    else:
        print("Data is empty!")


while True:
    time.sleep(100)
    print('tick')
