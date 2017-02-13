from datetime import datetime
import RPi.GPIO as GPIO
from RPLCD import CharLCD

class Display:
    def __init__ ( self ):
        self.lcdWidth = 20
        self.lcdHeight = 4
        self.displayText = []
        self.currentText = []
        self.currentPos = []
        self.lcd = CharLCD ( pin_rs=26,pin_rw=16,pin_e=20,pins_data=[5,6,13,19],numbering_mode=GPIO.BCM,cols=self.lcdWidth,rows=self.lcdHeight)
        self.updateDatetime = datetime.strptime ( 'Jun 1 1971 1:00PM', '%b %d %Y %I:%M%p' )
        for i in range ( self.lcdHeight ):
            self.displayText.append ( ' ' )
            self.currentText.append ( ' ' )
            self.currentPos.append ( 0 )
    def __del__ ( self ):
        self.lcd.close (clear=False)
    def setText ( self, newText ):
        if len ( newText ) < self.lcdHeight:
            return;
#        trKeys = self.translate.keys ()
        for ind in range ( self.lcdHeight ):
		self.currentText [ ind ] = newText [ ind ]
#            self.currentText [ ind ] ='';
#            for i in newText [ ind ]:
#                if i in trKeys:
#                    self.currentText [ ind ] += self.translate [ i ]
#                else:
#                    self.currentText [ ind ] += i
        for ind in range ( self.lcdHeight ):
            if self.currentText [ ind ] != self.displayText [ ind ]:
                self.currentPos [ ind ] = 0

    def updateLCD ( self ):
        self.currentDatetime = datetime.today ()
        if abs ( ( self.currentDatetime - self.updateDatetime ).microseconds ) < 200000:
            return
        for ind in range ( self.lcdHeight ):
            if self.currentText [ ind ] != self.displayText [ ind ] or len ( self.currentText [ ind ] ) > self.lcdWidth:
                self.displayText [ ind ] = self.currentText [ ind ]
                self.lcd.cursor_pos = ( ind, 0 )
                self.lcd.write_string ( self.getString ( ind ) )
        self.updateDatetime = datetime.today ()

    def getString ( self, index ):
        result = '';
        if len ( self.displayText [ index ] ) < self.lcdWidth:
            result = self.displayText [ index ];
            while ( len ( result ) < self.lcdWidth ):
                result += ' '
            return result
        result += self.displayText [ index ] [ self.currentPos [ index ] : self.currentPos [ index ] + self.lcdWidth ] + ' '
        if len ( result ) < self.lcdWidth:
            result += self.displayText [ index ] [ : ( self.lcdWidth - len ( result ) ) ]
        self.currentPos [ index ] += 1
        if self.currentPos [ index ] == len ( self.displayText [ index ] ):
            self.currentPos [ index ] = 0
        return result
