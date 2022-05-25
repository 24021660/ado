from ping3 import ping
import threading
from app.package_function import redis_client

class myThread (threading.Thread):
    def __init__(self, threadID, host_ip):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.host_ip = host_ip
    def run(self):
        ping_host(self.host_ip)


def ping_host(host_ip):
    print(host_ip)
    redis_client.hset('host_ping_status',host_ip,ping(host_ip))
    return 0

def get_host_list():
    return redis_client.lrange("host_list", 0, -1)

def ping_host_list():
    host_list=get_host_list()
    print(host_list)
    num=0
    for host_ip in host_list:
        num+=1
        thread=myThread(num, host_ip)
        thread.start()


