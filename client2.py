import os
import time
import sys
import serial 
from models.rfCards import *
from config import Config
import threading
import logging
from logging import handlers
import requests  
import json
import datetime
from apscheduler.schedulers.background import BackgroundScheduler


handler=handlers.TimedRotatingFileHandler("Rfid.log", when='W0',
                                                   backupCount=4,
                                                   utc=False)
logging.basicConfig(filename='Rfid.log',format=Config.FORMAT,level="DEBUG",handler=handler)
allLoc=LocationDetails.query.all()
allLoc=allLoc[0] if allLoc else {"id":"Not Set yet","gatewayId":"does not exists "}

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
        timestamp=datetime.datetime.strftime(time,"%d-%b-%y %H:%M:%S")
        if (data.get("status",False)):
            logging.info("Data insude %s",data["data"])        
            headers = {
            'Content-Type': 'application/json'
            }
            payload={                        
                        "school_code":allLoc.id,
                        "attendance_timestamp":timestamp,
                        "rf_id":data["data"],
                        "gwId":allLoc.gatewayId               
                    }
            logging.debug("payload is %s",payload)
            try:
                response = requests.request("POST", Config.url, headers=headers,
                                            data = json.dumps(payload))
                if (response.status_code!=200):
                    entry=Rfid(data["data"],time)
                    db.session.add(entry)
                    db.session.commit()                    
                logging.debug("response from server %s",response.text)
            except Exception as ex:
                logging.error("exception in server resp %s",ex)
                entry=Rfid(data["data"],time)
                db.session.add(entry)
                db.session.commit()                    

                
def schedulledJob():
    dataToSend=Rfid.query.filter_by(has_transfered=False).all()
    if (dataToSend):
        finalData=map(lambda data:{                        
            "school_code":allLoc.id,
            "attendance_timestamp":datetime.datetime.strftime(data.entryDate,"%d-%b-%y %H:%M:%S"),
            "rf_id":data.number,
            "gwId":allLoc.gatewayId               
           },dataToSend)
        logging.debug("pending data --> %s",finalData)
        headers = {
                'Content-Type': 'application/json'
                }
        response = requests.request("POST", Config.url, headers=headers,
                                data = json.dumps(finalData))
        if (response.status_code==200):
            for i in dataToSend:
                i.has_transfered=True
                db.session.add(i)
            db.session.commit()
            logging.info("pending data has been sent successfully")
    
    
        
t1=threading.Thread(target=start)
t1.start()
scheduler = BackgroundScheduler()
job = scheduler.add_job(schedulledJob, 'interval', minutes=Config.SCHEDULLE_TIME)
scheduler.start()


