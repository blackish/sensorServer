from datetime import datetime,timedelta

class ThermSensor ():
    def __init__ ( self, addr ):
        self.currentTemp = 0;
        self.therm = addr
        self.currentDatetime = datetime.strptime ( 'Jun 1 1971 1:00PM', '%b %d %Y %I:%M%p' )
    def getTemp ( self ):
        currentDatetime = datetime.today ()
        cTemp = self.currentTemp;
        if abs ( ( currentDatetime - self.currentDatetime ).seconds ) > 600:
            self.currentDatetime = datetime.today ()
            with open ( "/sys/bus/w1/devices/" + self.therm + "/w1_slave","r" ) as f:
                line = f.readline ()
                if line.find ( "YES" ) > -1: 
                    line = f.readline ()
                    s = line.split ( "t=" )
                    cTemp = eval ( s [ 1 ].rstrip () ) / 1000
                    if cTemp == 85:
                        cTemp = self.currentTemp
                    print "New temp", cTemp
                else:
                    currentTemp = 0
            self.currentTemp = cTemp
            self.currentTemp = self.currentTemp
            f.close ()
        else:
            cTemp = self.currentTemp;
        return cTemp
