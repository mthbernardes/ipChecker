import os
import requests
from db.db import Database
from lxml import html

class xroxy:
    def __init__(self,):
        self.db = Database()
        maxIndex = int(self.getmax())
        for index in range(0,maxIndex+1):
            tree = self.connect(index)
            raw = tree.xpath('//*[@title="View this Proxy details"]/text()')
            ips = [ip.strip() for ip in raw if ip.strip()]
            self.db.insert(ips)

    def connect(self,index):
        url = 'http://www.xroxy.com/proxylist.php?pnum=%d' % index
        r = requests.get(url,timeout=10)
        tree = html.fromstring(r.text)
        return tree

    def getmax(self,):
        tree = self.connect(0)
        maxIndex = int(tree.xpath('//*[@id="content"]/table[2]/tr/td[1]/table/tr[2]/td/small/b/text()')[0])/10
        return maxIndex

if __name__ == '__main__':
    xroxy()
