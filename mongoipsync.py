#!/usr/bin/python3
from secrets import uri

MYID = "tester"

import time
import threading
import requests
from pymongo.mongo_client import MongoClient

IPIFY = "http://api.ipify.org"

def myip():
    r = requests.get(url=IPIFY)
    data = r.content
    return data.decode().strip()

client = MongoClient(uri)

maincoll = client.ipsync.main

def changeip(ip=myip()):
    print("syncing IP: "+str({"id": MYID, "ip": ip}))
    maincoll.delete_many({"id": MYID})
    maincoll.insert_one({"id": MYID, "ip": ip})
    
defaultip = myip()
changeip(defaultip)

def getips():
	return maincoll

while True:
    newip = myip()
    print(f"IP: {newip}")
    print(f"OtherIPs: {tuple(maincoll.find())}")
    if newip != defaultip:
        defaultip = newip
        changeip(defaultip)
    time.sleep(30*60)
