import os
import requests
from db.db import Database

class rebroproxy:
    def __init__(self,):
        self.db = Database()
        url = 'http://rebro.weebly.com/uploads/2/7/3/7/27378307/rebroproxy-all-113326062014.txt'
        r = requests.get(url,timeout=10)
        ips = list()
        for raw in r.text.split():
            ips.append(raw.split(':')[0])
        self.db.insert(ips)

if __name__ == '__main__':
    rebroproxy()
