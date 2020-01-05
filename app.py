#!/usr/bin/env python

from flask import Flask, render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
import threading 
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
mail = Mail(app)
from models.rfCards import *


  

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000), debug=True)

