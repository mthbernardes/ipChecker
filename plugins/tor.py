#http://torstatus.blutmagie.de

import os
import requests
from db.db import Database
from lxml import html

class tor:
    def __init__(self,):
        self.db = Database()
        r = requests.get('http://torstatus.blutmagie.de/',timeout=10)
        tree = html.fromstring(r.content)
        torNodes = tree.xpath('//*[@class="who"]/text()')
        self.db.insert(torNodes)

if __name__ == '__main__':
    tor()
