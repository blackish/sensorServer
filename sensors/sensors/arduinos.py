import time

class Arduino:
    def __init__ ( self, addr, cursor, conn, init = [] ):
        self.address = addr
        self.CONN = conn
        self.CURSOR = cursor
        self.sensors = { "LCD": 0, "Thermo": 0, "Relay":0 }
        self.alarm = 0
        self.lcdText = [ ' ', ' ', ' ' ]
        self.lcdTextUpdated = [ True, True, True ]
        self.receiveBuffer = []
        self.lastUpdated = 0
        self.pendingDelete = 60000
        self.currentPending = 0
        self.initialized = False
        self.tempFix = 0
        self.toSend = [] #0 - request capabilities, 1 - request thermostate, 2 - update text, 3 - send relay cmd
        self.tempC = 255
        self.relayLow = 255
        self.relayHigh = 255
        self.relayStatus = 0
        self.remoteRelayStatus = 255
        self.CURSOR.execute ( "INSERT OR REPLACE INTO devices ( address, description, last_seen ) VALUES ( %d, (SELECT description FROM devices WHERE address=%d ), datetime ( 'now' ) )" % ( self.address, self.address ) )
        self.CONN.commit ()
        if len ( init ) > 0:
            self.receive ( init )
        print "Registered"
        print self.address
    def getAlarm ( self ):
        return self.alarm
    def getRelay ( self ):
        return self.sensors [ "Relay" ]
    def setLcdText ( self, text ):
        if len ( text ) < self.sensors [ "LCD" ] or self.sensors [ "LCD" ] < 1:
            return False
        for i in range ( len ( self.lcdText ) ):
            if self.lcdText [ i ] != text [ i ]:
                self.lcdText [ i ] = text [ i ]
                self.lcdTextUpdated [ i ] = False
                self.toSend.append ( 2 )
    def receive ( self, payload ):
        if not self.currentPending == 0:
            self.currentPending = 0
        flags = payload.pop ( 0 )
        if not len ( payload ) == 0:
            self.receiveBuffer += payload
        if flags & 1 == 1:
            packetTimer = 0
        if flags & 1 == 1 and len ( self.receiveBuffer ) > 0:
            self.workReceived ()
        if flags & 1 == 1 and not self.initialized and len ( self.receiveBuffer ) == 0:
            self.toSend.append ( 0 );
            print "RECEIVE: request capas"
        self.receiveBuffer = []
    def workReceived ( self ):
#cmd: 0 - receive capabilities, 1 - receive thermostate, 3 - receive relay status
        cmd = self.receiveBuffer.pop ( 0 )
        cmd = cmd + ( self.receiveBuffer.pop ( 0 ) << 8 )
        print "cmd"
        print cmd
        if not self.initialized and cmd > 0:
            self.receiveBuffer = []
            print "WORDRECEIVE: request capas"
            self.toSend.append ( 0 )
        if cmd == 0:
            try:
                capas = self.receiveBuffer.pop ( 0 )
                capas = capas + ( self.receiveBuffer.pop ( 0 ) << 8 )
                if capas & 1 == 1:
                    self.sensors [ "Thermo" ] = 1
                    self.CURSOR.execute ( "INSERT OR REPLACE INTO sensors ( device_id, sensor_type, value, fix_value, description ) VALUES ( %d, 1, 0, IFNULL(( SELECT fix_value FROM sensors WHERE device_id = %d AND sensor_type = 1 ),0), ( SELECT description FROM sensors WHERE device_id = %d and SENSOR_TYPE = 1 ) )" % ( self.address, self.address, self.address ) )
                    self.CONN.commit ()
                    print "Got Thermo"
                if capas & 2 == 2:
                    self.sensors [ "LCD" ] = self.receiveBuffer.pop ( 0 )
                    self.sensors [ "LCD" ] = self.sensors[ "LCD" ] + ( self.receiveBuffer.pop ( 0 ) << 8 )
                    print "Got LCD"
                if capas & 8 == 8:
                    self.sensors [ "Relay" ] = 1;
                    self.CURSOR.execute ( "INSERT OR REPLACE INTO sensors ( device_id, sensor_type, value, fix_value, description ) VALUES ( %d, 8, 0, IFNULL(( SELECT fix_value FROM sensors WHERE device_id = %d AND sensor_type = 8 ),0), ( SELECT description FROM sensors WHERE device_id = %d and SENSOR_TYPE = 8 ) )" % ( self.address, self.address, self.address ) )
                    self.CONN.commit ()
                    print "Got Relay"
                print "Initialized"
                self.initialized = True
            except IndexError:
                self.sensors [ "Thermo" ] = 0
                self.sensors [ "LCD" ] = 0
                self.initialized = False
        if cmd == 1:
            try:
                self.tempC = self.receiveBuffer.pop ( 0 )
                self.tempC = self.tempC + ( self.receiveBuffer.pop ( 0 ) << 8 )
                self.CURSOR.execute ( "UPDATE sensors SET value=%d WHERE device_id=%d AND sensor_type=1" % ( self.tempC, self.address ) )
                self.CURSOR.execute ( "UPDATE devices SET last_seen=datetime('now') WHERE address=%d" % self.address )
                self.CONN.commit ()
                print "Got temp", self.tempC
            except IndexError:
                self.tempC = 255
        if cmd == 3:
            try:
                self.relayLow = self.receiveBuffer.pop ( 0 )
                self.relayHigh = self.receiveBuffer.pop ( 0 )
                self.remoteRelayStatus = self.receiveBuffer.pop ( 0 )
                self.CURSOR.execute ( "UPDATE sensors SET value=%d WHERE device_id=%d AND sensor_type=8" % ( self.remoteRelayStatus, self.address ) )
                self.CURSOR.execute ( "UPDATE devices SET last_seen=datetime('now') WHERE address=%d" % self.address )
                self.CONN.commit ()
                print "Got relays!"
            except IndexError:
                self.relayLow = 255
                self.relayHigh = 255
                self.remoteRelayStatus = 255
                print "Relay error"
    def getPending ( self ):
        sendStr = ''
        if len ( self.toSend ) > 0:
            cmd = self.toSend.pop ( 0 )
            print "sending"
            print cmd
            sendStr += chr ( cmd & 255 ) + chr ( cmd >> 8 )
            if cmd == 2:
                try:
                    for i in range ( self.sensors [ "LCD" ] ):
                        if not self.lcdTextUpdated [ i ]:
                            sendStr = sendStr + chr ( i ) + self.lcdText [ i ]
                            self.lcdTextUpdated [ i ] = True
                            return sendStr
                except IndexError:
                    pass
            if cmd == 3:
                sendStr = sendStr + chr ( self.relayStatus )
                print self.relayStatus
                return sendStr
            if cmd == 1:
                self.CURSOR.execute ( "SELECT fix_value FROM sensors WHERE device_id=%d AND sensor_type=1" % self.address )
                row = self.CURSOR.fetchone ()
                if self.tempFix != int ( row [ 0 ] ):
                    self.tempFix = int ( row [ 0 ] )
                    sendStr = sendStr + chr ( int ( row [ 0 ] ) )
        print "Sending str"
        print sendStr
        return sendStr
    def checkTimers ( self ):
        ctime = int(round(time.time() * 1000))
        if not self.initialized:
            return
        if self.currentPending > 0:
            return
        if ctime - self.lastUpdated > 60000:
            if self.sensors[ "Thermo" ] > 0:
                self.toSend.append ( 1 )
            if self.sensors[ "Relay" ] > 0:
                self.toSend.append ( 3 )
            self.lastUpdated = int(round(time.time() * 1000))
    def setPending ( self ):
        if self.currentPending == 0:
            self.currentPending = int(round(time.time() * 1000 ) )
    def checkDead ( self ):
        if self.currentPending == 0:
            return False
        ctime = int(round(time.time() * 1000))
        if ctime - self.currentPending > self.pendingDelete:
            return True
