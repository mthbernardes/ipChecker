import os
import requests
from db.db import Database
from lxml import html

class hidemy:
    def __init__(self,):
        self.db = Database()
        try:
            maxIndex,totalPages = self.getIndex()
            for x in range(0,maxIndex,maxIndex/totalPages):
                content = self.connect(x)
                tree = html.fromstring(content)
                ips = tree.xpath('//*[@class="tdl"]/text()')
                ports = tree.xpath('//*[@id="content-section"]/section[1]/div/table/tbody/tr/td[2]/text()')
                self.db.insert(ips)
        except Exception as e:
            pass

    def connect(self,index):
        url = 'https://hidemy.name/en/proxy-list/?start=%d' % index
        r = requests.get(url,timeout=10)
        return r.content

    def getIndex(self,):
        content = self.connect(0)
        tree = html.fromstring(content)
        maxIndex = tree.xpath('//*[@id="content-section"]/section[1]/div/div[4]/ul/li/a/@href')[-1].split('=')[1].split('#')[0]
        totalPages = tree.xpath('//*[@id="content-section"]/section[1]/div/div[4]/ul/li/a/text()')[-1]
        return int(maxIndex),int(totalPages)

if __name__ == '__main__':
    hidemy()
