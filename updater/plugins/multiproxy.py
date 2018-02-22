import os
import requests
from db.db import Database

class multiproxy:
    def __init__(self,):
        self.db = Database()
        url = 'http://multiproxy.org/txt_all/proxy.txt'
        r = requests.get(url,timeout=10)
        ips = list()
        for raw in r.text.split():
            ips.append(raw.split(':')[0])
        self.db.insert(ips)

if __name__ == '__main__':
    multiproxy()
