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

from box0._binding import libbox0, ffi, string_converter
from box0.exceptions import ResultException
from box0.module import Ain, Aout, Spi, I2c, Dio, Pwm, Module
from box0.generic import *

def build_module_list(dev):
	result = []

	for i in range(dev._pointer.modules_len):
		mod = Module(dev._pointer, dev._pointer.modules[i])
		result.append(mod)

	return result

class Device(Base, Close):
	"""
	Box0 Device

	.. warning::
		Do not try to instantiate :class:`box0.Device`, instead use a backend
		(for example :class:`box0.usb`) to get a device, see the below code.

	.. code-block:: python

		import box0
		try:
			# open device
			dev = box0.usb.open_supported()

			# device information
			printf("Name: %s" % dev.name)
			printf("Manufacturer: %s" % dev.manuf)
			printf("Serial: %s" % dev.serial)

			# contained modules information
			for m in dev.modules:
				print("Found: %s", m.name)

			# close device
			dev.close()
		except ResultException, e:
			print("failed! (%s)" % e)
	"""

	_log = libbox0.b0_device_log
	_close = libbox0.b0_device_close

	_ping = libbox0.b0_device_ping

	LOG_DEBUG = libbox0.B0_LOG_DEBUG
	"""Debug log + INFO"""

	LOG_INFO = libbox0.B0_LOG_INFO
	"""Informational log + WARN"""

	LOG_WARN = libbox0.B0_LOG_WARN
	"""Warning log + ERROR"""

	LOG_ERROR = libbox0.B0_LOG_ERROR
	"""Error log only"""

	LOG_NONE = libbox0.B0_LOG_NONE
	"""No log"""

	name = None
	"""Printable device name"""

	manuf = None
	"""Printable manufacturer name"""

	serial = None
	"""Printable serial number"""

	modules = None
	"""
	Modules contained in the device.
	collection of :class:`box0.module.Module`
	"""

	def __init__(self, dev):
		"""
		Create a Device object from b0_device

		:param dev: libbox0 device
		:type dev: b0_device*
		"""
		Base.__init__(self, dev)
		self.name = string_converter(self._pointer.name)
		self.manuf = string_converter(self._pointer.manuf)
		self.serial = string_converter(self._pointer.serial)
		self.modules = build_module_list(self)

	def log(self, log_level):
		"""
		Set debug level for device

		:param int log_level: Log level of device
		:raises ResultException: if libbox0 return negative result code

		.. note::

			log can be overriden by enviroment variable "LIBBOX0_LOG".
			LIBBOX0_LOG accept ("0", "1", "2", "3", "4", "none", "error", "warn", "info", "debug")
		"""
		ResultException.act(self._log(self._pointer, log_level))

	def ain(self, index = 0):
		"""
		Open AIN module with `index`

		:param int index: Module index
		:return: the opened module
		:rtype: box0.module.Ain
		"""
		return Ain(self, index)

	def aout(self, index = 0):
		"""
		Open AOUT module with `index`

		:param int index: Module index
		:return: the opened module
		:rtype: box0.module.Aout
		"""
		return Aout(self, index)

	def pwm(self, index = 0):
		"""
		Open PWM module with `index`

		:param int index: Module index
		:return: the opened module
		:rtype: box0.module.Pwm
		"""
		return Pwm(self, index)

	def dio(self, index = 0):
		"""
		Open DIO module with `index`

		:param int index: Module index
		:return: the opened module
		:rtype: box0.module.Dio
		"""
		return Dio(self, index)

	def spi(self, index = 0):
		"""
		Open SPI module with `index`

		:param int index: Module index
		:return: the opened module
		:rtype: box0.module.Spi
		"""
		return Spi(self, index)

	def i2c(self, index = 0):
		"""
		Open I2C module with `index`

		:param int index: Module index
		:return: the opened module
		:rtype: box0.module.I2c
		"""
		return I2c(self, index)

	def ping(self):
		"""
		If no exceptions are raised,
		then it can be assured that the device is connected, and running properly.

		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._ping(self._pointer))

	def __str__(self):
		return self.name
