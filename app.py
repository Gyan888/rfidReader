#!/usr/bin/env python

from flask import Flask, render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
import threading 
from apscheduler.schedulers.background import BackgroundScheduler
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
mail = Mail(app)
ma = Marshmallow()
from models.rfCards import *



def test_job():
    print ("schedulled job")    

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(test_job, 'interval', minutes=1)
    scheduler.start()
    rfSchema=RfSchema(many=True)
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000), debug=True)

