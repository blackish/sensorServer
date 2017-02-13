#!/usr/bin/python

import time
from I2C_RPi import I2C_RPi

class BMP085:

	i2c = None
	# Operating Modes
  	__BMP085_ULTRALOWPOWER     = 0
  	__BMP085_STANDARD          = 1
  	__BMP085_HIGHRES           = 2
  	__BMP085_ULTRAHIGHRES      = 3

  	#Coefs
  	_AC1 = 0
  	_AC2 = 0
  	_AC3 = 0
  	_AC4 = 0
  	_AC5 = 0
  	_AC6 = 0
  	_B1 = 0
  	_B2 = 0
  	_MB = 0
  	_MC = 0
  	_MD = 0

	def __init__(self, address=0x77, mode=1):
    		self.i2c = I2C_RPi(address)
    		self.address = address    
    		# Make sure the specified mode is in the appropriate range
    		if ((mode < 0) | (mode > 3)):
    			self.mode = self.__BMP085_STANDARD
    		else:
    			self.mode = mode
    		# Read the calibration data
    		self.readCoef()

	def readCoef(self):
		self._AC1 = self.i2c.read_s16(0xAA)
		self._AC2 = self.i2c.read_s16(0xAC)
		self._AC3 = self.i2c.read_s16(0xAE)
		self._AC4 = self.i2c.read_u16(0xB0)
		self._AC5 = self.i2c.read_u16(0xB2)
		self._AC6 = self.i2c.read_u16(0xB4)
		self._B1 = self.i2c.read_s16(0xB6)
		self._B2 = self.i2c.read_s16(0xB8)
		self._MB = self.i2c.read_s16(0xBA)
		self._MC = self.i2c.read_s16(0xBC)
		self._MD = self.i2c.read_s16(0xBE)

	def readRawTemp(self):
		self.i2c.write_8(0xF4, 0x2E)
		time.sleep(0.005)
		raw_UT = self.i2c.read_u16(0xF6)
		return raw_UT

	def readTemp(self):
		UT = 0
		X1 = 0
		X2 = 0
		B5 = 0
		T_C = 0
		#self.i2c.write_8(0xF4, 0x2E)
		#time.sleep(0.005)
		UT = self.readRawTemp() #self.i2c.read_u16(0xF6)
		X1 = ((UT - self._AC6) * self._AC5) >> 15
		X2 = (self._MC << 11) / (X1 + self._MD)
		B5 = X1 + X2
		T = ((B5 + 8) >> 4) / 10.0
		return T

	def readRawPressure(self):
		self.i2c.write_8(0xF4, 0x34 + (self.mode << 6))
		if (self.mode == self.__BMP085_ULTRALOWPOWER):
			time.sleep(0.005)
		elif (self.mode == self.__BMP085_HIGHRES):
			time.sleep(0.014)
		elif (self.mode == self.__BMP085_ULTRAHIGHRES):
			time.sleep(0.026)
		else:
			time.sleep(0.008)
		raw_UP_MSB = self.i2c.read_u8(0xF6)
		raw_UP_LSB = self.i2c.read_u8(0xF7)
		raw_UP_XLSB = self.i2c.read_u8(0xF8)
		#raw pressure
		raw_UP = ((raw_UP_MSB << 16) + (raw_UP_LSB << 8) + raw_UP_XLSB) >> (8 - self.mode)
		return raw_UP

	def readPressure(self):
		UP = 0
		UT = 0
		B3 = 0
		B4 = 0
		B5 = 0
		B7 = 0
		X1 = 0
		X2 = 0
		X3 = 0
		p = 0		
		
		#calculating pressure in Pascals
		UT = self.readRawTemp()
		UP = self.readRawPressure()
		
		X1 = ((UT - self._AC6) * self._AC5) >> 15
		X2 = (self._MC << 11) / (X1 + self._MD)
		B5 = X1 + X2
		B6 = B5 - 4000
		X1 = (self._B2 * (B6 * B6) >> 12) >> 11
		X2 = (self._AC2 * B6) >> 11
		X3 = X1 + X2
		B3 = (((self._AC1 * 4 + X3) << self.mode) + 2) / 4

		X1 = (self._AC3 * B6) >> 13
		X2 = (self._B1 * ((B6 * B6) >> 12)) >> 16
		X3 = ((X1 + X2) + 2) >> 2
		B4 = (self._AC4 * (X3 + 32768)) >> 15
		B7 = (UP - B3) * (50000 >> self.mode)

		if (B7 < 0x80000000):
			p = (B7 * 2) / B4
		else:
			p = (B7 / B4) * 2

		X1 = (p >> 8) * (p >> 8)
		X1 = (X1 * 3038) >> 16
		X2 = (-7375 * p) >> 16

		p = p + ((X1 + X2 + 3791) >> 4)
		return p
		
	def readAltitude(self):
		altitude = 0
		p0 = 101325 #sea level pressure
		pressure = float(self.readPressure())		
		altitude = 44330.0 * (1.0 - pow(pressure / p0, 0.1903))
		return altitude

