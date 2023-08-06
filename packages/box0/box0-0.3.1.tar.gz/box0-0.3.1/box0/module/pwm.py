#
# This file is part of pyBox0.
# Copyright (C) 2014, 2015 Kuldeep Singh Dhaka <kuldeep@madresistor.com>
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

from box0.module import ModuleInstance
from box0.module.module import speed_set, speed_get, bitsize_get, bitsize_set
from box0.exceptions import ResultException
from box0._binding import libbox0, ffi, cast_to_array, string_array_converter,\
							DummyObject

class Pwm(ModuleInstance):
	_close = libbox0.b0_pwm_close
	_open = libbox0.b0_pwm_open

	_width_get = libbox0.b0_pwm_width_get
	_width_set = libbox0.b0_pwm_width_set
	_period_set = libbox0.b0_pwm_period_set
	_period_get = libbox0.b0_pwm_period_get
	_speed_set = libbox0.b0_pwm_speed_set
	_speed_get = libbox0.b0_pwm_speed_get
	_bitsize_set = libbox0.b0_pwm_bitsize_set
	_bitsize_get = libbox0.b0_pwm_bitsize_get

	_output_prepare = libbox0.b0_pwm_output_prepare
	_output_start = libbox0.b0_pwm_output_start
	_output_stop = libbox0.b0_pwm_output_stop
	_output_calc = libbox0.b0_pwm_output_calc

	pin_count = None
	"""Number of pins"""

	label = None
	"""String related to module (Names of pin in `self.label.pin`)"""

	ref = None
	"""Reference.
		Attributes:
		`high`: HIGH_VALUE
		`low`: LOW_VALUE
		`type`: TYPE_OF_REFERENCE
	"""

	bitsize = None
	"""Supported bitsize"""

	speed = None
	"""Supported speeds"""

	def __init__(self, dev, index):
		ModuleInstance.__init__(self, dev, index, "b0_pwm**")
		self.pin_count = self._pointer.pin_count
		self.label = DummyObject()
		self.label.pin = string_array_converter(self._pointer.label.pin, \
							self._pointer.pin_count)
		self.bitsize = cast_to_array("unsigned int", self._pointer.bitsize)
		self.speed = cast_to_array("unsigned long", self._pointer.speed)
		self.ref = self._pointer.ref

	def output_calc(self, bitsize, freq, max_error = 100.0, best_result=False):
		speed_ptr = ffi.new("uint32_t*")
		period_ptr = ffi.new("b0_pwm_reg*")

		ResultException.act(self._output_calc(self._pointer, bitsize, freq, \
								speed_ptr, period_ptr, max_error, best_result))

		return (speed_ptr[0], period_ptr[0])

	def output_prepare(self):
		ResultException.act(self._output_prepare(self._pointer))

	def output_start(self):
		ResultException.act(self._output_start(self._pointer))

	def output_stop(self):
		ResultException.act(self._output_stop(self._pointer))

	def period_get(self):
		val_ptr = ffi.new("b0_pwm_reg*")
		ResultException.act(self._period_get(self._pointer, val_ptr))
		return val_ptr[0]

	def period_set(self, value):
		ResultException.act(self._period_set(self._pointer, value))

	def width_set(self, index, value):
		ResultException.act(self._width_set(self._pointer, index, value))

	def width_get(self, index):
		val_ptr = ffi.new("b0_pwm_reg*")
		ResultException.act(self._width_get(self._pointer, index, val_ptr))
		return val_ptr[0]

	@staticmethod
	def output_calc_width(period, duty_cycle):
		"""
		Calculate width value from period and duty cycle.
		:param period: Period
		:param duty_cycle: Duty Cycle (0 <= duty_cycle <= 100)
		:return: Width value
		"""
		assert(0 < duty_cycle < 100)
		return int((float(period) * float(duty_cycle)) / 100.0)

	@staticmethod
	def output_calc_duty_cycle(period, width):
		"""
		Calculate Duty cycle value from period and width
		:param period: Period
		:param width: Width
		:return: Duty cycle
		"""
		return (float(width) * 100.0) / float(period)

	@staticmethod
	def output_calc_freq(speed, period):
		"""
		Calculate frequency from period and speed
		:param speed: Speed
		:param period: Period
		:return: Frequency
		"""
		return float(speed) / float(period)

	@staticmethod
	def output_calc_freq_err(required_freq, calc_freq):
		"""
		Calculate error.
		:param required_freq: Required frequency (user need)
		:param calc_freq: Calculated frequency (user can have)
		:return: Error (in percentage)
		.. note::

			*Relative error*
		"""
		assert(calc_freq > 0)
		assert(required_freq > 0)
		calc_freq = float(calc_freq)
		required_freq = float(required_freq)
		dev = abs(calc_freq - required_freq)
		return (dev * 100.0) / required_freq

	speed_set = speed_set
	speed_get = speed_get

	bitsize_set = bitsize_set
	bitsize_get = bitsize_get
