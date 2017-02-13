#!/usr/bin/python

from flask_script import Manager
from app import model, app, db
import datetime
if __name__ == "__main__":

#    SM = model.SensorType ()
#    SM.sensor_type_id = 1
#    SM.sensor_name = "Thermometer"
#    db.session.add ( SM )
#    db.session.commit ()
#    scheduler = model.Schedulers ()
#    scheduler.is_active = True

#    heatsched = model.HeatScheduler ()
#    heatsched.start_time = datetime.time ( 7 )
#    heatsched.end_time = datetime.time ( 19 )
#    heatsched.thigh = 13
#    heatsched.tlow = 10
#    heatsched.dow = 15
#    scheduler.heatscheduler.append ( heatsched )
#    heatsched = model.HeatScheduler ()
#    heatsched.start_time = datetime.time ( 7 )
#    heatsched.end_time = datetime.time ( 17 )
#    heatsched.thigh = 13
#    heatsched.tlow = 10
#    heatsched.dow = 16
#    scheduler.heatscheduler.append ( heatsched )
    
#    db.session.add ( scheduler )
#    db.session.add ( heatsched )
#    db.session.commit ()

#    t = datetime.time ( 7 )
#    print t
    s = model.Schedulers.query.get ( 1 )
    for i in s.heatscheduler:
        print i.start_time
    u = model.Devices.query.all ()
    for uu in u:
        for i in uu.sensors:
            print i.description
#    for i in s.heatscheduler.all ():
#        if t >= i.start_time:
#            print "more"
#        else:
#            print "not"
#        print i.start_time
