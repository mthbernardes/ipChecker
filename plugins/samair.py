import os
import requests
from db.db import Database
from lxml import html

class samair:
    def __init__(self,):
        self.db = Database()
        maxIndex = self.maxIndex()
        for index in range(0,maxIndex+1):
            self.get(index)

    def maxIndex(self,):
        url = "http://samair.ru/proxy/"
        r = requests.get(url,timeout=10)
        tree = html.fromstring(r.content)
        indexes = tree.xpath('//*[@id="navbar"]/ul/li/a/text()')
        indexes.pop()
        return int(indexes[-1])

    def get(self,index):
        url = 'http://samair.ru/proxy/list-IP-port/proxy-%d.htm' % index
        r = requests.get(url,timeout=10)
        tree = html.fromstring(r.content)
        raw = tree.xpath('//div[@class="singleprice order-msg"]/pre/text()')
        if raw:
            raw.pop(0)
            raw = raw[0].split('\n')
            ips = [ip.split(':')[0] for ip in raw if ip]
            self.db.insert(ips)

if __name__ == '__main__':
    samair()
