#www.gatherproxy.com

import os
import requests
from db.db import Database
from lxml import html
from threading import Thread

class gatherproxy:
    def __init__(self,):
        self.db = Database()
        countries = self.getCountries()
        for country in countries:
            t = Thread(target=self.proxybyCountry, args=(country,))
            t.start()

    def proxybyCountry(self,country):
        country = country.strip()
        maxIndex = self.totalPages(country)
        for index in range(1,maxIndex+1):
                self.getProxies(country,index)

    def getCountries(self,):
        url = 'http://www.gatherproxy.com/proxylistbycountry'
        r = requests.get(url,timeout=10)
        tree = html.fromstring(r.content)
        countries = [country.split('(')[0] for country in tree.xpath('//*[@class="pc-list"]/li/a/text()')]
        return countries

    def connect(self,country,index):
        url = 'http://www.gatherproxy.com/proxylist/country/?c=%s' % country
        data = {'Country':country,'Filter':'','PageIdx':index,'Uptime':0}
        r = requests.post(url,data=data,timeout=10)
        return r.content

    def totalPages(self,country):
        try:
            content = self.connect(country,1)
            tree = html.fromstring(content)
            maxIndex = tree.xpath('//*[@id="psbform"]/div/a/text()')
            if maxIndex:
                return int(maxIndex[-1])
            else:
                return 0
        except Exception as e:
            pass

    def getProxies(self,country,index):
        content = self.connect(country,index)
        tree = html.fromstring(content)
        try:
            ips = [ip.split("document.write('")[1].split("')")[0] for ip in tree.xpath('//*[@id="tblproxy"]/tr/td[2]/script/text()')]
            self.db.insert(ips)
        except Exception as e:
            pass

if __name__ == '__main__':
    gatherproxy()
