#coding=UTF8
import urllib
from xml.dom import minidom
from datetime import datetime,timedelta

class Weather:
    def __init__ ( self ):
        self.currentWeather = u' ';
        self.currentDatetime = datetime.strptime ( 'Jun 1 1971 1:00PM', '%b %d %Y %I:%M%p' )
    def getWeather ( self ):
        cWeather = u' '
        currentDatetime = datetime.today ()
        if abs ( ( currentDatetime - self.currentDatetime ).seconds ) > 1440:

            try:
                f = urllib.urlopen ( "http://api.openweathermap.org/data/2.5/forecast/daily?id=524901&appid=&mode=xml&lang=ru&units=metric" )
                xmldoc = minidom.parse ( f )
                f.close ()
                if len ( xmldoc.childNodes ) <= 0:
                    currentWeather = u' '
                    return currentWeather
                self.currentDatetime = datetime.today ()

                cWeather = u'Сегодня '
                day = xmldoc.firstChild.childNodes [ 4 ].firstChild
                cWeather += day.getElementsByTagName ( 'symbol' )[ 0 ].attributes [ 'name' ].value
                cWeather += u', P='
                cWeather += "%d" % int ( float ( day.getElementsByTagName ( 'pressure' )[ 0 ].attributes [ 'value' ].value ) * 0.75006 )
                cWeather += u', W='
                cWeather += "%d" % int ( float ( day.getElementsByTagName ( 'windSpeed' )[ 0 ].attributes [ 'mps' ].value ) )
                cWeather += day.getElementsByTagName ( 'windDirection' )[ 0 ].attributes [ 'code' ].value
                cWeather += u', H='
                cWeather += day.getElementsByTagName ( 'humidity' )[ 0 ].attributes [ 'value' ].value
                cWeather += u'%, днем '
                cWeather += "%d" % int ( float ( day.getElementsByTagName ( 'temperature' )[ 0 ].attributes [ 'day' ].value ) )
                cWeather += u'\xb0C'
                cWeather += u', ночью '
                cWeather += "%d" % int ( float ( day.getElementsByTagName ( 'temperature' )[ 0 ].attributes [ 'night' ].value ) )
                cWeather += u'\xb0C. Завтра '
                day = day.nextSibling
                cWeather += day.getElementsByTagName ( 'symbol' )[ 0 ].attributes [ 'name' ].value
                cWeather += u', P='
                cWeather += "%d" % int ( float ( day.getElementsByTagName ( 'pressure' )[ 0 ].attributes [ 'value' ].value ) * 0.75006 )
                cWeather += u', W='
                cWeather += "%d" % int ( float ( day.getElementsByTagName ( 'windSpeed' )[ 0 ].attributes [ 'mps' ].value ) )
                cWeather += day.getElementsByTagName ( 'windDirection' )[ 0 ].attributes [ 'code' ].value
                cWeather += u', H='
                cWeather += day.getElementsByTagName ( 'humidity' )[ 0 ].attributes [ 'value' ].value
                cWeather += u'%, днем '
                cWeather += "%d" % int ( float ( day.getElementsByTagName ( 'temperature' )[ 0 ].attributes [ 'day' ].value ) )
                cWeather += u'\xb0C'
                cWeather += u', ночью '
                cWeather += "%d" % int ( float ( day.getElementsByTagName ( 'temperature' )[ 0 ].attributes [ 'night' ].value ) )
                cWeather += u'\xb0C'

                self.currentWeather = cWeather
            except Exception:
                cWeather = u'Погода недоступна'
        	self.currentDatetime = datetime.strptime ( 'Jun 1 1971 1:00PM', '%b %d %Y %I:%M%p' )
                self.currentWeather = cWeather
        else:
            cWeather = self.currentWeather;
        return cWeather
