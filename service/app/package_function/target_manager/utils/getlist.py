import time

def get1(c):
    return c[0]
def get2(c):
    return c[1]


def get_now_time(now_timestamp):
    timeArray = time.localtime(now_timestamp)
    otherStyleTime = time.strftime("%H:%M:%S", timeArray)
    return otherStyleTime