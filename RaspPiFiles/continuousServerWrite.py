import time
import serial
import csv
import string
from pymongo import MongoClient
from random import randint
from pprint import pprint

from bson.objectid import ObjectId
client = MongoClient('mongodb+srv://admin:0urtnknM5IpkGQcV@4g06parkme-4gwxq.mongodb.net/test?retryWrites=true')
db=client.ParkMe

collection = db.get_collection('ParkingLots')
id1 = '5c49470d78dea5feb9d02a2c'
ser = serial.Serial('/dev/ttyACM0',9600,timeout=None)
file = open ("dataFile.txt", "w")

#sensorID0 = '5c4946c9ac8f790000f001cf';
#sensorID1 = '5c4be566bc01840000b851d3';
#sensorID2 = '5c534fd3a2b1de00000ed7a3';
#sensorID3 = '5c53504ea2b1de00000ed7a4';


spotState = False;
while True:

    # gets current time in ms
    eventTime = int(round(time.time()*1000))

    data = ser.readline()

    data = data.decode().replace("b'","")
    data = data.replace("\r\n'","")
    event = data.split(",")
    event[1].replace("\r\n","")
    
    if (event[0] != ""):
        #print( "exact string: " + event[1], flush=True)
        if ("1" in str(event[1])):
            spotState = True;
        else:
            spotState = False;
        #print(spotState, flush=True)
        log = {'_id': ObjectId(event[0]), 'time': eventTime, 'occupancy': spotState};
        #print(log, flush=True)
        if (str(event[0]) == '5c4946c9ac8f790000f001cf'):
            print("Sensor(0) 1,1: " + str(spotState));
        elif (str(event[0]) == '5c4be566bc01840000b851d3'):
            print("Sensor(1) 1,2 : " + str(spotState));
        elif (str(event[0]) == '5c534fd3a2b1de00000ed7a3'):
            print("Sensor(2) 2,2: " + str(spotState));
        elif (str(event[0]) == '5c53504ea2b1de00000ed7a4'):
            spotState = False;
            print("Sensor(3) 3,3: " + str(spotState));
            
        result = collection.update_one({"_id":ObjectId(id1),"parking_spaces.id": ObjectId(event[0])}, {"$set": {"parking_spaces.$.occupancy": spotState}});
        result = collection.update_one({"_id":ObjectId(id1),"parking_spaces.id": ObjectId(event[0])}, {"$push": {"parking_spaces.$.logs": log}})
        #print("spot status update: " + str(result.modified_count), flush=True)
