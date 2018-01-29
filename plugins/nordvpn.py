#https://nordvpn.com/

import os
import requests
from db.db import Database

class nordvpn:
    def __init__(self,):
        self.db = Database()
        url = 'https://nordvpn.com/wp-admin/admin-ajax.php?searchParameters[0][name]=proxy-country&searchParameters[0][value]=&searchParameters[1][name]=proxy-ports&searchParameters[1][value]=&offset=0&limit=100000&action=getProxies'
        r = requests.get(url,timeout=10)
        ips = list()
        for proxy in r.json():
            ips.append(proxy['ip'])
        self.db.insert(ips)

if __name__ == '__main__':
    nordvpn()
