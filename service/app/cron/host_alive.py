import requests

def host_alive():
    requests.get(url='http://10.1.69.43:8090/computer_manager/host_ping_alive')

host_alive()