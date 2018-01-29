import os
import requests
from db.db import Database
from lxml import html

class cloudproxies:
    def __init__(self,):
        self.db = Database()
        maxIndex = self.getIndex()
        for index in range(1,maxIndex+1):
            self.getProxy(index)

    def connect(self,index):
        url = 'http://cloudproxies.com/proxylist/?page=%d' % index
        r = requests.get(url,timeout=10)
        return r.content

    def getIndex(self,):
        content = self.connect(1)
        tree = html.fromstring(content)
        maxIndex = tree.xpath('//*[@class="pagination"]/li/a/@data-ci-pagination-page')[-1]
        return int(maxIndex)

    def getProxy(self,index):
        content = self.connect(index)
        tree = html.fromstring(content)
        ip = tree.xpath('//*[@id="ContentTable"]/tbody/tr/td[3]/text()')
        port = tree.xpath('//*[@id="ContentTable"]/tbody/tr/td[4]/a/text()')
        if ip:
            self.db.insert(ip)

if __name__ == '__main__':
    cloudproxies()
