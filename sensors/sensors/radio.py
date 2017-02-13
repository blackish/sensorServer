from RF24 import *

class Radio:
    def __init__ ( self ):
        self.retries = 10
        self.timeout = 500
        self.maxPayload = 29
        self.receiveBuffer = [ u'', u'', u'', u'', u'' ]
#        self.r = RF24( RPI_V2_GPIO_P1_15, RPI_BPLUS_GPIO_J8_24, BCM2835_SPI_SPEED_8MHZ)
        self.r = RF24( RPI_V2_GPIO_P1_15, RPI_BPLUS_GPIO_J8_24, BCM2835_SPI_SPEED_8MHZ)
        self.r.begin ()
        self.r.enableDynamicPayloads ()
        self.r.setRetries ( 15, 15 )
        self.r.setChannel ( 0x4c )
        self.r.printDetails ()
        self.listenPipes = [ 0x3101010201, 0x3101010202, 0x301010203, 0x3101010204, 0x3101010205 ]
        self.addressMap = { 1: 0x3101010101 }
        for i in range ( 4 ):
            self.r.openReadingPipe ( i + 1, self.listenPipes [ i ] )
        self.r.startListening ()
    def receivePayload ( self ):
        
        if not self.r.available ():
            return list ( [] )
        receivePipe = self.r.available_pipe ()
        if not receivePipe [ 0 ]:
            return list ( [] )
        addr = 0
        payloadLen = self.r.getDynamicPayloadSize()
        buf = list ( bytearray ( self.r.read ( payloadLen ) ) )
        addr = buf.pop ( 0 )
        addr = addr + ( buf.pop ( 0 ) << 8 )
        if not addr in self.addressMap:
            self.addressMap [ addr ] = 0x3100000000 + ( ( self.listenPipes [ receivePipe [ 1 ] - 1 ] & 0x000000ffff ) << 16 ) + ( ( self.listenPipes [ receivePipe [ 1 ] - 1 ] & 0x00ffff0000 ) >> 16 )
            print self.addressMap [ addr ]
            print addr
        return list ( [ addr, buf ] )
    def sendPayload ( self, payload, address ):
        if len ( payload ) == 0:
            return True
        if not address in self.addressMap:
            return False
        segment = 0
        cretries = 0
        self.r.openWritingPipe ( self.addressMap [ address ] )
        self.r.stopListening ()
        while len ( payload ) > ( segment + 1 ) * self.maxPayload:
            buf = chr ( address & 255 ) + chr ( address >> 8 ) + chr ( 0 ) + payload [ segment * self.maxPayload : ( segment + 1 ) * self.maxPayload ];
            cretries = 0
            sentSuccess = False
            while sentSuccess == False and cretries < self.retries:
                sentSuccess = self.r.write ( buf )
                cretries += 1
            if not sentSuccess:
                return False
            segment += 1
        buf = chr ( address & 255 ) + chr ( address >> 8 ) + chr ( 1 ) + payload [ segment * self.maxPayload : ]
        cretries = 0
        sentSuccess = False
        while sentSuccess == False and cretries < self.retries:
            sentSuccess = self.r.write ( buf )
            cretries += 1
        self.r.startListening ()
        if not sentSuccess:
            print "Failed"
            return False
        return True
