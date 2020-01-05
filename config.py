import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'rfTables.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEVELOPMENT = True
    DEBUG = False
    CORS_HEADERS='Content-Type'
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = "***"
    MAIL_PASSWORD= "****"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    HOSTNAME="localhost"
    CLIENT_port=1883
    CLIENT_topic="/home/rfid/{}"
    url = "http://api.sbsy.in/api/Attendance/MarkUserAttendance"
    FORMAT = '%(asctime)-15s   %(message)s'
    SCHEDULLE_TIME=30
