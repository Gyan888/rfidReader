import os
import time
import sys
import serial 
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from config import Config
from models.rfCards import *
import threading
allLoc=LocationDetails.query.all()  
allLoc=allLoc[0] if allLoc else {id:None}


def start():          
    while(1):      
        data=read_rfid()
        if (data.get("status",False)):
                print ("Data insude ",data["data"],Config.CLIENT_topic.format(allLoc.id))            
                client.publish(Config.CLIENT_topic.format(allLoc.id),data["data"], qos=2, retain=False)                        
            else:
                print("data not received ")
        
        


