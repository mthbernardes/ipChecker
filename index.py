"""A API REST to validated malicious IP's"""
import os
import hug
from db.db import Database
from threading import Thread
from hug_middleware_cors import CORSMiddleware

api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api))

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
    files = os.listdir('plugins')
    plugins = [plugin for plugin in files if '__' not in plugin]
    plugins = [plugin.replace('.py','') for plugin in plugins if '.pyc' not in plugin]
    return {'ips':totalIps,'requests':totalRequests,'allowed':totalAllowed,'blocked':totalBlocked,'plugins':plugins,'total_plugins':len(plugins)}
