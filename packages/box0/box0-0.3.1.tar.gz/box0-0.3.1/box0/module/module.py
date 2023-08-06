#
# This file is part of pyBox0.
# Copyright (C) 2014-2016 Kuldeep Singh Dhaka <kuldeep@madresistor.com>
#
# pyBox0 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyBox0 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyBox0.  If not, see <http://www.gnu.org/licenses/>.
#

from box0.exceptions import ResultException
from box0._binding import libbox0, ffi, string_converter, cast_to_array
from box0.generic import Base, Close
import numpy as np

class Module(Base):
	DIO = libbox0.B0_DIO
	AOUT = libbox0.B0_AOUT
	AIN = libbox0.B0_AIN
	SPI = libbox0.B0_SPI
	I2C = libbox0.B0_I2C
	PWM = libbox0.B0_PWM

	_OK = libbox0.B0_OK
	_ERR_UNAVAIL = libbox0.B0_ERR_UNAVAIL

	_openable = libbox0.b0_module_openable

	index = None
	"""Module index"""

	type = None
	"""Module type"""

	name = None
	"""Printable name of type"""

	def __init__(self, dev, mod):
		Base.__init__(self, mod)
		self.device = dev
		if hasattr(mod, 'header'):
			mod = mod.header

		self.index = mod.index
		self.type = mod.type
		self.name = string_converter(mod.name)

	def open(self):
		open_fn = {
			self.DIO: self.device.dio,
			self.AOUT: self.device.aout,
			self.AIN: self.device.ain,
			self.SPI: self.device.spi,
			self.I2C: self.device.i2c,
			self.PWM: self.device.pwm
		}.get(self.type)

		if open_fn is None:
			raise Exception("Module not supported")

		return open_fn(self.index)

	def openable(self):
		"""
		Return true if the module is openable
		:return bool: result
		:raises ResultException: if libbox0 return negative result code
		"""
		r = self._openable(self._pointer)
		if r == self._OK:
			return True
		elif r == self._ERR_UNAVAIL:
			return False

		ResultException.act(r)

	def __str__(self):
		return self.name

class ModuleInstance(Module, Close):
	"""
	Abstract class
	just, to keep out common code of modules

	Note:
	it is expected that, self._{load, unload, module}
		attributes will be added by sub class
	"""
	_open = None

	def __init__(self, dev, index, cdefstr):
		"""Construct a b0_<module> object"""
		mod_ptr = ffi.new(cdefstr)
		ResultException.act(self._open(dev._pointer, mod_ptr, index))
		mod = mod_ptr[0]
		Module.__init__(self, dev, mod)

	def open(self):
		raise Exception("Module is a instance")

	def openable(self):
		raise Exception("You already have the module opened!")

def bitsize_speed_set(self, bitsize, speed):
	ResultException.act(self._bitsize_speed_set(self._pointer, bitsize, speed))

def bitsize_speed_get(self):
	bitsize = ffi.new("unsigned int *")
	speed = ffi.new("unsigned long *")
	ResultException.act(self._bitsize_speed_get(self._pointer, bitsize, speed))
	return bitsize[0], speed[0]

def chan_seq_get(self):
	# Try to find the sequence which contain the full
	# channel sequence
	target = self.chan_count + 1
	while True:
		count = ffi.new("size_t", target)
		values = ffi.new("unsigned int []", target)
		ResultException.act(self._chan_seq_get(self._pointer, values, count))
		if count[0] < target:
			return cast_to_array("unsigned int", values, count[0])
		self.chan_count *= 2

def chan_seq_set(self, value):
	values = ffi.new("unsigned int []", value)
	ResultException.act(self._chan_seq_set(self._pointer, values, len(value)))

def speed_set(self, value):
	ResultException.act(self._speed_set(self._pointer, value))

def speed_get(self):
	value = ffi.new("unsigned long *")
	ResultException.act(self._speed_get(self._pointer, value))
	return value[0]

def bitsize_set(self, value):
	ResultException.act(self._bitsize_set(self._pointer, value))

def bitsize_get(self):
	value = ffi.new("unsigned int *")
	ResultException.act(self._bitsize_get(self._pointer, value))
	return value[0]
