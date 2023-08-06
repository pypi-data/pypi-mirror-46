#
# This file is part of pyBox0.
# Copyright (C) 2018 Kuldeep Singh Dhaka <kuldeep@madresistor.com>
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
from box0.driver.driver import Driver
from box0.module import I2c
from box0.exceptions import ResultException

class Bmp180(Driver):
	"""
	BMP180 (Pressure sensor) Driver
	"""

	OVER_SAMP_1 = libbox0.B0_BMP180_OVER_SAMP_1
	OVER_SAMP_2 = libbox0.B0_BMP180_OVER_SAMP_2
	OVER_SAMP_4 = libbox0.B0_BMP180_OVER_SAMP_4
	OVER_SAMP_8 = libbox0.B0_BMP180_OVER_SAMP_8

	_open = libbox0.b0_bmp180_open
	_over_samp_set = libbox0.b0_bmp180_over_samp_set
	_close = libbox0.b0_bmp180_close
	_read = libbox0.b0_bmp180_read

	def __init__(self, module):
		drv = ffi.new("b0_bmp180 **")
		ResultException.act(self._open(module._pointer, drv))

		"""Cache the objects"""
		Driver.__init__(self, drv[0], module)

	def over_samp_set(self, value):
		ResultException.act(self._over_samp_set(self._pointer, value))

	def read(self):
		arr = ffi.new("double [2]")
		ResultException.act(self._read(self._pointer, arr+0 , arr+1))
		return (arr[0], arr[1])
