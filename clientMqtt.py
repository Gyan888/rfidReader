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


def mqttProcess():

    def on_log(client, userdata, level, buf):
        print ("This is the buffer {}".format(buf))


    def on_publish(client, obj, mid):
        print("This is the  mid In on Pub call back: " + str(mid))

    def on_message(client, userdata, msg):
        print ("######################")
        print ("Topic: ", msg.topic + '  Message: ' + str(msg.payload))
        print ("######################")


    def read_rfid():   
        ser = serial.Serial ("/dev/ttyUSB0")                           #Open named port 
        ser.baudrate = 9600                                            #Set baud rate to 9600
        data = ser.read(12)                                            #Read 12 characters from serial port to data
        ser.close()                                                   #Close port               
        return {"data":data,"status":200} 

    def start():          
        while(1):      
            data=read_rfid()
            if (data.get("status",False)):
                print ("Data insude ",data["data"],Config.CLIENT_topic.format(allLoc.id))            
                client.publish(Config.CLIENT_topic.format(allLoc.id),data["data"], qos=2, retain=False)                        
            else:
                print("data not received ")
        
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        print ("Making Default Values____________________________________________________")
        client.subscribe("/home/rfid/1")
        threading.Thread(target=start).start()
        
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_log = on_log
    #client.tls_set('/etc/ssl/certs/ca-certificates.crt',tls_version=2)
    #client.username_pw_set(Config.CLIENT_username,Config.CLIENT_password)
    client.connect(Config.HOSTNAME, Config.CLIENT_port, 60)
    client.loop_forever()

mqttProcess()
