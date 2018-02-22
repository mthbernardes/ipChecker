"""A API REST to validated malicious IP's"""
import hug
from db.db import Database

api = hug.API(__name__)

@hug.get('/ips')
def find(ip):
    """Validate if the IP is malicious"""
    db = Database()
    result = db.find(ip)
    if result:
        db.statsInsert(ip,'blocked')
        return {'isMalicious':True}
    else:
        db.statsInsert(ip,'allowed')
        return {'isMalicious':False}

@hug.get('/all',output=hug.output_format.text)
def allips():
    """Get all ips"""
    db = Database()
    totalIps = '\n'.join([ip.ip for ip in db.total()])
    return totalIps

@hug.post('/ips')
def insert(ips:hug.types.json):
    """Search for a IP on the mailicious IP database"""
    db = Database()
    db.insert(ips)
    return {'message':True}

@hug.delete('/ips')
def delete(ips:hug.types.json):
    """Delete a IP from the mailicious IP database"""
    db = Database()
    db.delete(ips)
    return {'message':True}

@hug.get('/statistics')
def total():
    """Get statistics about the application"""
    db = Database()
    totalIps = len(db.total())
    totalRequests,totalAllowed,totalBlocked = db.statistics()
    return {'ips':totalIps,'requests':totalRequests,'allowed':totalAllowed,'blocked':totalBlocked}
