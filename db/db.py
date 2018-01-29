import time
from pydal import DAL, Field
from datetime import datetime

class Models(object):
    def __new__(self,):
        #username,passwd,host,port = os.getenv('DATABASE_USERNAME'),os.getenv('DATABASE_PASSWORD'),os.getenv('DATABASE_HOST'),os.getenv('DATABASE_PORT')
        #dalString  = 'mongodb://%s:%s@%s:%s/ipChecker' % (username,passwd,host,port) #uncomment to use mongodb
        dalString  = 'sqlite://ipChecker.db'  #uncomment to use sqlite
        db = DAL(dalString,migrate=True)
        db.define_table('ips',
            Field('ip'),
            Field('created_at',default=datetime.now().strftime("%d/%m/%Y")),
            Field('cloudflare','boolean',default=False))
        db.define_table('statistics',
            Field('ip'),
            Field('status'),
            Field('created_on','datetime', default=datetime.now))
        return db

class Database(object):
    def insert(self,ip):
        db = Models()
        if type(ip) == list:
            for x in ip:
                db.ips.update_or_insert((db.ips.ip==x)&(db.ips.created_at==datetime.now().strftime("%d/%m/%Y")),ip=x)
        else:
            db.ips.update_or_insert(ip=ip)
        db.commit()

    def delete(self,ip):
        db = Models()
        if type(ip) == list:
            for x in ip:
                db(db.ips.ip == x).delete()
        else:
            db(db.ips.ip == ip).delete()
        db.commit()

    def statsInsert(self,ip,status):
        db = Models()
        db.statistics.insert(ip=ip,status=status)
        db.commit()

    def statistics(self):
        db = Models()
        totalRequests = db(db.statistics.id > 0).count()
        totalBlocked = db(db.statistics.status == 'blocked').count()
        totalAllowed = totalRequests - totalBlocked
        return totalRequests,totalAllowed,totalBlocked

    def total(self,):
        db = Models()
        total = db(db.ips.created_at==datetime.now().strftime("%d/%m/%Y")).select()
        return total

    def getIpsToCloudFlare(self,):
        db = Models()
        allIps = db((db.ips.cloudflare == False) & (db.ips.created_at==datetime.now().strftime("%d/%m/%Y"))).select()
        return allIps

    def sentToCloudFlare(self,ip):
        db = Models()
        allIps = db((db.ips.ip == ip) & (db.ips.created_at==datetime.now().strftime("%d/%m/%Y"))).update(cloudflare=True)
        db.commit()

    def find(self,ip):
        db = Models()
        ip = db((db.ips.ip == ip) & (db.ips.created_at==datetime.now().strftime("%d/%m/%Y"))).select()
        return ip
