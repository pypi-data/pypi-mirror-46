# -*- coding: utf-8 -*-

#
# This file is part of pyBox0.
# Copyright (C) 2015, 2016 Kuldeep Singh Dhaka <kuldeep@madresistor.com>
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

from box0._binding import libbox0, ffi
from box0.exceptions import ResultException
from box0 import Device

class Box0V5PowerSupply(Device):
	"""box0-v5 power supply specific functionality"""

	_ps_en_set = libbox0.b0v5_ps_en_set
	_ps_en_get = libbox0.b0v5_ps_en_get
	_ps_oc_get = libbox0.b0v5_ps_oc_get
	_ps_oc_ack = libbox0.b0v5_ps_oc_ack

	PS_PM5 = libbox0.B0V5_PS_PM5
	"""±5V power supply mask"""

	PS_P3V3 = libbox0.B0V5_PS_P3V3
	"""+3.3V power supply mask"""

	PS_ANALOG = libbox0.B0V5_PS_PM5
	"""Analog power supply (alias of `PM5`)"""

	PS_DIGITAL = libbox0.B0V5_PS_P3V3
	"""Digital power supply (alias of `P3V3`)"""

	def ps_en_set(self, mask, value):
		"""
		Enable power supply

		:param mask: Mask for power supply to change
		:param value: Value of the power supply whose crossponding mask has been set

		:raises ResultException: if C function return libusb error code
		"""
		ResultException.act(self._ps_en_set(self._pointer, mask, value))

	def ps_en_get(self):
		"""
		Get the power supply enable status

		:return int: mask of power supply enabled

		:raises ResultException: if C function return libusb error code
		"""
		val_ptr = ffi.new("uint8_t*")
		ResultException.act(self._ps_en_get(self._pointer, val_ptr))
		return val_ptr[0]

	def ps_oc_get(self):
		"""
		Get power supply over-current status

		:return int: mask for power supply in over-current condition

		:raises ResultException: if C function return libusb error code
		"""
		val_ptr = ffi.new("uint8_t*")
		ResultException.act(self._ps_oc_get(self._pointer, val_ptr))
		return val_ptr[0]

	def ps_oc_ack(self, mask):
		"""
		Acknowledge power supply over-current condition

		:param mask: Mask for power supply to Acknowledge for

		:raises ResultException: if C function return libusb error code
		"""
		ResultException.act(self._ps_oc_ack(self._pointer, mask))
