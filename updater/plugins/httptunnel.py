import os
import requests
from db.db import Database
from lxml import html

class httptunnel:
    def __init__(self,):
        self.db = Database()
        url = 'http://www.httptunnel.ge/ProxyListForFree.aspx'
        r = requests.get(url,timeout=10)
        tree = html.fromstring(r.content)
        raw = tree.xpath('//*[@target="_new"]/text()')
        ips = [ip.split(':')[0] for ip in raw]
        self.db.insert(ips)

if __name__ == '__main__':
    httptunnel()
