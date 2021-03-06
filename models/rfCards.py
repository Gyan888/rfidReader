from app import db,ma
import datetime
class Rfid(db.Model):
    __tablename__ = "rfidScanned"    
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String())
    has_transfered=db.Column(db.Boolean, default=False, nullable=False)
    entryDate=db.Column(db.DateTime)    
    
   
    def __repr__(self):
        return '<number {}>'.format(self.number)
    
    def __init__(self,SeatName):
        self.number=number
        self.entryDate = datetime.datetime.now()

class LocationDetails(db.Model):
    __tablename__="LocationDetails"
    id = db.Column(db.Integer, primary_key=True)
    locationName=db.Column(db.String(),unique=True)
    createdDate=db.Column(db.DateTime)
    
    def __repr__(self):
        return '<locationName {}>'.format(self.locationName)

    
    def __init__(self,name):
        self.locationName=name
        self.createdDate = datetime.datetime.now()
        

class RfSchema(ma.Schema):
    class Meta:
        fields = ('number', 'has_transfered',"locationName")