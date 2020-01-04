import os
import time
import sys
import serial 
from models.rfCards import *
from config import Config
import threading
allLoc=LocationDetails.query.all()
import requests  
import json
allLoc=allLoc[0] if allLoc else {id:"Not Set yet",gatewayId:"does not exists "}
import datetime


def read_rfid():   
    ser = serial.Serial ("/dev/ttyUSB0")                           #Open named port 
    ser.baudrate = 9600                                            #Set baud rate to 9600
    data = ser.read(12)                                            #Read 12 characters from serial port to data
    ser.close()                                                   #Close port               
    return {"data":data,"status":200} 



def start():          
    while(1):      
        data=read_rfid()
        time=datetime.datetime.now()
        timestamp=datetime.datetime.strftime(time,"%d-%b-%y %h:%m:%s")
        if (data.get("status",False)):
            print ("Data insude ",data["data"])
            payload={                        
                        "school_code":alloc.id,
                        "attendance_timestamp":timestamp
                        "rfId":data["data"].
                        "gwId":alloc.gatewayId               
                    }
            headers = {
                     'Content-Type': 'application/json'
                    }
            try:
                response = requests.request("POST", Config.url, headers=headers,
                                            data = json.dumps(payload))
                print ("response from server ",response)
            except(ex):
                print ("exception in server resp ",response)
                    

        
start()

