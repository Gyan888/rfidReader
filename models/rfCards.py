from app import db
import datetime
class Rfid(db.Model):
    __tablename__ = "rfidScanned"    
    id = db.Column(db.Integer(), primary_key=True)
    number = db.Column(db.String())
    has_transfered=db.Column(db.Boolean(), default=False, nullable=False)
    entryDate=db.Column(db.DateTime())    
    
   
    def __repr__(self):
        return '<number {},has_transfered {},time:{}>'.format(self.number,
                                                              self.has_transfered,
                                                              self.entryDate)
    
    def __init__(self,number,entryDate):
        self.number=number                
        self.entryDate=entryDate
        self.has_transfered=False

class LocationDetails(db.Model):
    __tablename__="LocationDetails"
    id = db.Column(db.Integer(), primary_key=True)
    gatewayId=db.Column(db.Integer(), unique=True)
    locationName=db.Column(db.String())
    createdDate=db.Column(db.DateTime())
    
    def __repr__(self):
        return '<locationName {}>'.format(self.locationName)

    
    def __init__(self,name,gatewayId):
        self.locationName=name
        self.createdDate = datetime.datetime.now()
        self.gatewayId=gatewayId
        

