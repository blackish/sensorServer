#!/usr/bin/python
#i2c lib for RPi v.1.0

import time
import smbus

class I2C_RPi:
	def __init__(self, address, bus=smbus.SMBus(1)):
    		self.address = address
    		self.bus = bus
	def read_u8(self, reg_addr):
		try:
			rezult = self.bus.read_byte_data(self.address, reg_addr)
			return rezult
		except IOError, err:
			print "Error accessing 0x%02X: Check your I2C address" % self.address
		return -1

	def read_u16(self, reg_addr):
		try:
			MSB_byte = self.bus.read_byte_data(self.address, reg_addr)
			LSB_byte = self.bus.read_byte_data(self.address, reg_addr + 1)
			rezult = (MSB_byte << 8) + LSB_byte
			return rezult
		except IOError, err:
			print "Error accessing 0x%02X: Check your I2C address" % self.address
			return -1

	def read_s16(self, reg_addr):    
    		try:
    			MSB_byte = self.bus.read_byte_data(self.address, reg_addr)
    			LSB_byte = self.bus.read_byte_data(self.address, reg_addr + 1)
    			if (MSB_byte > 127):
        			MSB_byte -= 256
    			rezult = (MSB_byte << 8) + LSB_byte      
    			return rezult
    		except IOError, err:
    			print "Error accessing 0x%02X: Check your I2C address" % self.address
    			return -1

	def write_8(self, reg_addr, value):
		try:
			self.bus.write_byte_data(self.address, reg_addr, value)
		except IOError, err:
			print "Error accessing 0x%02X: Check your I2C address" % self.address
			return -1
