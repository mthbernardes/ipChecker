import os
import base64
import requests
from db.db import Database
from lxml import html

class proxylist:
    def __init__(self,):
        self.db = Database()
        maxIndex = self.getMax()
        for index in range(0,maxIndex+1):
            self.getproxy(index)

    def connect(self,index):
        url = 'https://proxy-list.org/english/index.php?p=%d' % index
        r = requests.get(url,timeout=10)
        tree = html.fromstring(r.text)
        return tree

    def getMax(self,):
        tree = self.connect(1)
        indexes = tree.xpath('//*[@id="content"]/div[4]/div[5]/div[2]/a/text()')
        indexes.pop()
        return int(indexes[-1])

    def getproxy(self,index):
        tree = self.connect(index)
        raw = [base64.b64decode(ip.split("('")[1].split("')")[0]) for ip in tree.xpath('//*[@class="proxy"]/script/text()')]
        ips = list()
        for info in raw:
            ips.append(info.decode().split(':')[0])
        self.db.insert(ips)

if __name__ == '__main__':
    proxylist()
