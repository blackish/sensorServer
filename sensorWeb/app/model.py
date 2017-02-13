#!/usr/bin/python

from app import db
from flask.ext.login import UserMixin

class Configs ( db.Model ):
    __tablename__ = 'configs'
    cname = db.Column ( db.String ( 128 ), primary_key = True )
    value = db.Column ( db.String ( 128 ) )

class SensorType ( db.Model ):
    __tablename__ = "sensor_type"
    sensor_type_id = db.Column ( db.Integer, primary_key = True )
    sensor_name = db.Column ( db.String ( 128 ) )

class Devices ( db.Model ):
    __tablename__ = "devices"
    address = db.Column ( db.Integer, primary_key = True )
    description = db.Column ( db.String ( 128 ) )
    last_seen = db.Column ( db.DateTime )
    sensors = db.relationship ( 'Sensors', backref = 'devices', lazy = 'joined' )

class Sensors ( db.Model ):
    __tablename__ = "sensors"
    device_id = db.Column ( db.Integer, db.ForeignKey ( "devices.address" ) )
    sensor_type = db.Column ( db.Integer, db.ForeignKey ( "sensor_type.sensor_type_id" ) )
    value = db.Column ( db.Float )
    fix_value = db.Column ( db.Float )
    description = db.Column ( db.String ( 128 ) )
    __table_args__ = ( db.PrimaryKeyConstraint ( 'device_id', 'sensor_type' ), )

class Users ( db.Model, UserMixin ):
    __tablename__ = "users"
    user_id = db.Column ( db.String ( 128 ), primary_key = True )
    passwd = db.Column ( db.String ( 128 ) )
    def get_id ( self ):
        return self.user_id

class HeatScheduler ( db.Model ):
    __tablename__ = "heatscheduler"
    id = db.Column ( db.Integer, primary_key = True )
    start_time = db.Column ( db.Time )
    end_time = db.Column ( db.Time )
    dow = db.Column ( db.Integer )
    thigh = db.Column ( db.Integer )
    tlow = db.Column ( db.Integer )
    scheduler_id = db.Column ( db.Integer, db.ForeignKey ( 'schedulers.id' ) )

class Schedulers ( db.Model ):
    __tablename__ = "schedulers"
    id = db.Column ( db.Integer, primary_key = True )
    is_active = db.Column ( db.Boolean )
    descr = db.Column ( db.String ( 128 ) )
    heatscheduler = db.relationship ( 'HeatScheduler', backref = 'schedulers', lazy = 'joined' )

class Weather ( db.Model ):
    __tablename__ = "weather"
    id = db.Column ( db.Integer, primary_key = True )
    weather = db.Column ( db.String ( 255 ) )

