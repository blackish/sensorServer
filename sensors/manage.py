#coding=UTF8
from datetime import datetime
from sensors.therm import ThermSensor
from sensors.weather import Weather
from sensors.lcd import Display
import time
from sensors.BMP085_device import BMP085
import RPi.GPIO as GPIO
from subprocess import call
from sensors.radio import Radio
from sensors.trans import Trans
from sensors.arduinos import Arduino
import socket
import sqlite3
import os

CONN = sqlite3.connect ( 'sensors.db' )
CURSOR = CONN.cursor ()


Tlow = 255
Thigh = 255

def loadConfig ():
    global Tlow, Thigh, CURSOR
    CURSOR.execute ( 'SELECT * FROM configs WHERE cname="tlow"' )
    row = CURSOR.fetchone ()
    if not row == None:
        Tlow = int ( row [ 1 ] )
    CURSOR.execute ( 'SELECT * FROM configs WHERE cname="thigh"' )
    row = CURSOR.fetchone ()
    if not row == None:
        Thigh = int ( row [ 1 ] )

def run ():
    global Tlow, Thigh
    print os.getpid ()

    print ( "New Tlow is:" )
    print ( Tlow )
    print ( "New Thigh is:" )
    print ( Thigh )

#    INQ = Q
    sendDatetime = datetime.strptime ( 'Jun 1 1971 1:00PM', '%b     %d %Y %I:%M%p' )
    thermDatetime = datetime.strptime ( 'Jun 1 1971 1:00PM', '%b     %d %Y %I:%M%p' )
    weatherDatetime = datetime.strptime ( 'Jun 1 1971 1:00PM', '%b     %d %Y %I:%M%p' )
    timeDatetime = datetime.strptime ( 'Jun 1 1971 1:00PM', '%b     %d %Y %I:%M%p' )
    currentDatetime = datetime.strptime ( 'Jun 1 1971 1:00PM', '%b     %d %Y %I:%M%p' )
    narodmonDatetime = datetime.strptime ( 'Jun 1 1971 1:00PM', '%b     %d %Y %I:%M%p' )
    thermLimit = 60
    weatherLimit = 3600
    timeLimit = 30
    sendLimit = 5
    killPin = 27
    NARODMON_MAC = ''
    SENSOR_ID_1 = NARODMON_MAC + '01'
    SENSOR_ID_2 = NARODMON_MAC + '02'
    SENSOR_ID_3 = NARODMON_MAC + '03'
    narodmonLimit = 900
    
    screen = [ u' ', u' ', u' ', u' ' ]
    temp = 0
    tempOut = 0
    bar = 0
    alt = 0
    weather = u' '
    cdate = u' '
    sensor = ThermSensor ( '28-00043e3599ff' )
    sensorOut = ThermSensor ( '28-00043e2fcaff' )
    weatherPredict = Weather ()
    temp = sensor.getTemp () - 2
    tempOut = sensorOut.getTemp ()
    myLcd = Display ()
    barometer = BMP085(0x77, 1)
    GPIO.setmode ( GPIO.BCM )
    GPIO.setup ( killPin, GPIO.IN )
    radio = Radio ()
    tr = Trans ()
    remotes = {}
    received = []
    
    screen [ 3 ] = u' '
    updated = False;
    
    loadConfig ()
    while True:
        currentDatetime = datetime.today ()
        if abs ( ( currentDatetime - thermDatetime ).seconds ) >= thermLimit:
            thermDatetime = currentDatetime
            temp = sensor.getTemp () - 2
            tempOut = sensorOut.getTemp ()
            CURSOR.execute ( "UPDATE sensors SET value=%d WHERE device_id=0 AND sensor_type=1" % ( temp + 2 ) )
            CURSOR.execute ( "UPDATE sensors SET value=%d WHERE device_id=0 AND sensor_type=65538" % tempOut )
            CONN.commit ()
            try:
                bar = (int)(barometer.readPressure () * 0.0075)
                CONN.commit ()
                alt = barometer.readAltitude ()
            except ValueError:
                alt = 0
                print "Error getting preasure"
            CURSOR.execute ( "UPDATE sensors SET value=%d WHERE device_id=0 AND sensor_type=65537" % bar )
            screen [ 1 ] = u'Tд=' + str ( temp ) + u'\xb0C Tу=' + str ( tempOut ) + u'\xb0C P=' + str ( bar )
            updated = True
#        if abs ( ( currentDatetime - weatherPredict.currentDatetime ).seconds ) >= weatherLimit:
        if abs ( ( currentDatetime - weatherDatetime ).seconds ) >= weatherLimit:
            weatherDatetime = currentDatetime
            print "Requesting weather"
            currentWeather = weatherPredict.getWeather ()
            screen [ 2 ] = currentWeather
#            screen [ 2 ] = u'Тут будет электро'
            updated = True
            CURSOR.execute ( "INSERT OR REPLACE INTO weather VALUES ( 0, '%s' )" % ( currentWeather ) )
        if abs ( ( currentDatetime - timeDatetime ).seconds ) >= timeLimit:
            timeDatetime = currentDatetime
            cdate = u'  ' + currentDatetime.strftime ( "%H:%M %d.%m.%Y" )
            screen [ 0 ] = cdate
            updated = True
        if updated:
            myLcd.setText ( tr.translateUTF ( screen ) )
            print screen [ 0 ]
            print screen [ 1 ]
            print screen [ 2 ]
            print screen [ 3 ]
        myLcd.updateLCD ()
        if abs ( ( currentDatetime - narodmonDatetime ).seconds ) >= narodmonLimit:
            narodmonDatetime = currentDatetime
            try:
                sock = socket.socket ()
                sock.connect ( ( 'narodmon.ru', 8283 ) )
                sock.send ( "#{}\n#{}#{}\n#{}#{}\n#{}#{}\n##".format ( NARODMON_MAC, SENSOR_ID_1, tempOut, SENSOR_ID_2, bar, SENSOR_ID_3, temp ) )
                data = sock.recv ( 1024 )
                sock.close ()
                print "NARODMON sent"
                print data
            except socket.error, e:
                print "ERROR!"
        if GPIO.input ( killPin ):
            call ( [ "killall", "kodi.bin" ] )
            print "kill pressed"
        rkeys = remotes.keys ()
        if radio.r.available ():
            received = radio.receivePayload ()
            try:
                if len ( received ) == 2:
                    if received [ 0 ] in remotes:
                        remotes [ received [ 0 ] ].receive ( received [ 1 ] )
                    else:
                        remotes [ received [ 0 ] ] = Arduino ( received [ 0 ], CURSOR, CONN, received [ 1 ] )
                        updated = True
                        CONN.commit ()
            except IndexError:
                print "Receive unknown"
        relay = []
        for k in rkeys:
            remotes [ k ].checkTimers ()
            if remotes [ k ].sensors [ "Relay" ] == 1:
                relay.append ( k )
            if updated:
                if remotes [ k ].sensors [ "LCD" ] > 0:
                    sensorLCD = [ u'', u'', u'', u'' ]
                    sensorLCD [ 0 ] = screen [ 0 ]
                    if remotes [ k ].sensors [ "Thermo" ] != 0:
                        CURSOR.execute ( "SELECT ( value - fix_value ) FROM sensors WHERE device_id=%d AND sensor_type=1" % remotes [ k ].address )
                        row = CURSOR.fetchone ()
                        sensorLCD [ 1 ] = u'Тд=' + "{0:d}".format ( int ( row [ 0 ] ) ) + u'\xb0C '
                    sensorLCD [ 1 ] = sensorLCD [ 1 ] + u'Ту=' + "{0:d}".format ( tempOut ) + u'\xb0C P=' + "{0:d}".format ( bar ) + u' '
                    sensorLCD [ 2 ] = screen [ 2 ] + u' '
                    remotes [ k ].setLcdText ( tr.translate ( sensorLCD ) )

        relayScreen = u''
        loadConfig ()
        CURSOR.execute ( "select h.tlow, h.thigh from heatscheduler h left join schedulers s on s.id = h.scheduler_id where s.is_active and h.start_time <= '%s' and h.end_time >= '%s' and h.dow & %d > 0" % ( currentDatetime.strftime ( "%H:%M" ), currentDatetime.strftime ( "%H:%M" ), 1 << currentDatetime.weekday () ) )
        row = CURSOR.fetchone ()
        if row is None:
            TlowWork = Tlow
            ThighWork = Thigh
        else:
            TlowWork = row [ 0 ]
            ThighWork = row [ 1 ]

#        CURSOR.execute ( "SELECT min ( value - fix_value ) FROM sensors WHERE sensor_type=1" )
        CURSOR.execute ( "select min(s.value - s.fix_value) from sensors s left join devices d on d.address=s.device_id where s.sensor_type=1 and ( ( julianday ( 'now' ) - julianday ( d.last_seen ) ) * 1440 < 5 or d.address = 0 )" )
        row = CURSOR.fetchone ()
        if relay:
            for k in relay:
#            print TlowWork
#            print ThighWork
#        if lowestTemp < remotes [ k ].relayLow and remotes [ k ].relayLow != 255:
                if TlowWork == 255:
                    TlowWork = remotes [ k ].relayLow
                if row [ 0 ] < TlowWork and remotes [ k ].relayStatus == 1 and TlowWork != 255:
                    remotes [ k ].relayStatus = 0
                    print "Change status to 1"
#        if lowestTemp > remotes [ k ].relayHigh and remotes [ k ].relayHigh != 255:
                if ThighWork == 255:
                    ThighWork = remotes [ k ].relayHigh
                if row [ 0 ] > ThighWork and remotes [ k ].relayStatus == 0 and ThighWork != 255:
                    remotes [ k ].relayStatus = 1
                    print "Change status to 0"
                relayScreen = u'Tlo=' + "{0:d}".format ( TlowWork ) + u'\xb0C Thi=' + "{0:d}".format ( ThighWork ) + u'\xb0C '
                if remotes [ k ].remoteRelayStatus == 0:
                    relayScreen += u'\xd9'
                relayScreen += u'*'
            if relayScreen != screen [ 3 ]:
                screen [ 3 ] = relayScreen
                updated = True
                myLcd.setText ( tr.translateUTF ( screen ) )
        if abs ( ( currentDatetime - sendDatetime ).seconds ) >= sendLimit:
            sendDatetime = currentDatetime
            deadList = []
#            try:
            for k in rkeys:
                if len ( remotes [ k ].toSend ) > 0:
                    if not radio.sendPayload ( remotes [ k ].getPending (), remotes [ k ].address ):
                        remotes [ k ].setPending ()
                if remotes [ k ].checkDead ():
                    deadList.append ( k )
#                        del remotes [ k ]
#            except IndexError:
#                print "Arduino is dead"
            if len ( deadList ) > 0:
                try:
                    while True:
                        del remotes [ deadList.pop () ]
                except IndexError:
                    print "Error deleting dead"
        updated = False

#        if not INQ.empty ():
#            cmd = INQ.get ( False )
#            if cmd == 'CHANGE_CONFIG':
#                loadConfig ()

def closeGPIO ():
    GPIO.cleanup ()

if __name__ == "__main__":
    loadConfig ()
    run ()
    closeGPIO ()
