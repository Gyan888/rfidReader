import os
import time
import sys
import serial 
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from config import Config
from models.rfCards import *
allLoc=LocationDetails.query.all()  
allLoc=allLoc[0] if allLoc else {id:None}


def read_rfid():   
    ser = serial.Serial ("/dev/ttyUSB0")                           #Open named port 
    ser.baudrate = 9600                                            #Set baud rate to 9600
    data = ser.read(12)                                            #Read 12 characters from serial port to data
    ser.close ()                                                   #Close port   
    return {"data":data,"status":200} 

def start():    
    while(True):
        data=read_rfid()
        if (data.get("status",False)):
            print ("Data insude ",data["data"])
            publish.single(Config.CLIENT_topic.format(allLoc.id), payload=data["data"], qos=2, retain=False, hostname=Config.HOSTNAME,
                       port=Config.CLIENT_port, client_id="", keepalive=60, will=None,tls=None, 
                       protocol=mqtt.MQTTv31,auth={'username':Config.CLIENT_username, 'password':Config.CLIENT_password})
            print ("Message sent successfuly")

        else:
            print("data not received ")
            
print ("starting the process")
start()