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

from box0._binding import ffi, libbox0, cast_to_array, string_converter, DummyObject
from box0.exceptions import ResultException
from box0.module import ModuleInstance
from box0.module.module import speed_set, speed_get
import numpy as np

def _to_cflags(mode, lsb_first, cpol, cpha):
	"""
	Convert value to mode flags
	"""
	_flags = 0

	if mode is not None:
		if cpol is not None:
			raise Exception("cpol and mode cannot exists together")
		if cpha is not None:
			raise Exception("cpha and mode cannot exists together")
		_mode = {
			0: libbox0.B0_SPI_TASK_MODE0,
			1: libbox0.B0_SPI_TASK_MODE1,
			2: libbox0.B0_SPI_TASK_MODE2,
			3: libbox0.B0_SPI_TASK_MODE3,
		}.get(mode)
		if _mode is None: raise Exception("Invalid SPI mode %i" % mode)
		_flags |= _mode
	else:
		if cpol: _flags |= libbox0.B0_SPI_TASK_CPOL
		if cpha: _flags |= libbox0.B0_SPI_TASK_CPHA

	if lsb_first:
		_flags |= libbox0.B0_SPI_TASK_LSB_FIRST

	return _flags

class Slave(object):
	def __init__(self, addr, mod, bitsize=None, speed=0, lsb_first=False, \
					mode=None, cpha=None, cpol=None):
		self.addr = addr
		self.mod = mod
		self._arg = ffi.new("b0_spi_sugar_arg *", {
			'flags': _to_cflags(mode, lsb_first, cpol, cpha),
			'addr': addr,
			'bitsize': bitsize,
			'speed': speed
		})

	def hd_write(self, data):
		self.mod.hd_write(self._arg, data)

	def hd_read(self, data):
		return self.mod.hd_read(self._arg, data)

	def fd(self, write, read):
		return self.mod.fd(self._arg, write, read)

	@property
	def active_state(self):
		return self.mod.active_state(self.addr)

	@active_state.setter
	def active_state(self, value):
		self.mod.active_state(self.addr, value)

	def __str__(self):
		return "Slave Address: " + hex(self.addr)

def _task_cflags(task):
	"""
	Convert the task flags to C flags
	"""

	_flags = 0

	if 'write' in task and 'read' in task:
		_flags |= libbox0.B0_SPI_TASK_FD
	elif 'write' in task:
		_flags |= libbox0.B0_SPI_TASK_HD_WRITE
	elif 'read' in task:
		_flags |= libbox0.B0_SPI_TASK_HD_READ
	else:
		raise Exception("Provide something to do (read, write or both)")

	flags = []

	for name in ('flag', 'flags'):
		if name not in task:
			continue
		data = task[name]
		if type(data) in (list, tuple):
			flags.extend(data)
		else:
			flags.append(data)

	for flag in flags:
		if flag.lower() in ('hd_write', 'hd_read', 'hd'):
			raise Exception("Library automatically infer transfer (%s)" % flag)

		if flag.lower() is 'last':
			raise Exception("LAST flag is automatically inferred")

		# FIXME: check if the two flags that modify same bit is provided
		_flag = {
			'mode0': libbox0.B0_SPI_TASK_MODE0,
			'mode1': libbox0.B0_SPI_TASK_MODE1,
			'mode2': libbox0.B0_SPI_TASK_MODE2,
			'mode3': libbox0.B0_SPI_TASK_MODE3,
			'lsb_first': libbox0.B0_SPI_TASK_LSB_FIRST,
			'msb_first': libbox0.B0_SPI_TASK_MSB_FIRST,
			'cpol': libbox0.B0_SPI_TASK_CPOL,
			'cpha': libbox0.B0_SPI_TASK_CPHA
		}.get(flag.lower())

		if _flag is None: raise Exception("Unknown flag %s" % flag)
		_flags |= _flag

	return _flags

def _bitsize_heuristic(data1, data2=None):
	dtype = None
	if data1 is None or data2 is None:
		data = data1 if data2 is None else data2
		dtype = data.dtype
	else:
		if data1.dtype == data2.dtype:
			dtype = data1.dtype

	if dtype is not None and dtype.itemsize > 0:
		return dtype.itemsize

	raise Exception("Please specify bitsize")

def _count_heuristic(data1, data2=None):
	if data1 is None or data2 is None:
		data = data1 if data2 is None else data2
		return len(data)
	else:
		if data1.dtype == data2.dtype:
			return min(len(data1), len(data2))

	raise Exception("Please specify count")

def _to_ctasks(tasks):
	"""
	Convert the python style task to C task
	"""

	if type(tasks) not in (list, tuple):
		# make it an iterable object
		tasks = [tasks]

	if not len(tasks): raise Exception("Tasks cannot be empty")

	_tasks = []
	for task in tasks:
		write = task['write']
		read = task['read']

		count = task['count'] \
			if 'count' in task else _count_heuristic(write, read)

		bitsize = task['bitsize'] \
			if 'bitsize' in task else _bitsize_heuristic(write, read)

		speed = task['speed'] if 'speed' in task else 0

		write_buf = ffi.cast("void *", write.ctypes.data) \
				if write is not None else ffi.NULL
		read_buf = ffi.cast("void *", read.ctypes.data) \
				if read is not None else ffi.NULL

		# check for overflow
		_bytes = np.floor(count * bitsize / 8.0)
		if write is not None: assert(write.nbytes >= _bytes)
		if read is not None: assert(read.nbytes >= _bytes)
		_tasks.append({
			'flags': _task_cflags(task),
			'bitsize': bitsize,
			'speed': speed,
			'addr': task['addr'],
			'wdata': write_buf,
			'rdata': read_buf,
			'count': count
		})

	_tasks[-1]['flags'] |= libbox0.B0_SPI_TASK_LAST
	return ffi.new("b0_spi_task []", _tasks)

def _to_sugar_arg(arg):
	if type(arg) is dict:
		return ffi.new("b0_spi_sugar_arg *", {
			'arg': arg['arg'],
			'bitsize': arg['bitsize'],
			'flags': arg['flags'],
			'speed': arg['speed'] if 'speed' in arg else 0
		})
	return arg

class Spi(ModuleInstance):
	_open = libbox0.b0_spi_open
	_close = libbox0.b0_spi_close

	_active_state_get = libbox0.b0_spi_active_state_get
	_active_state_set = libbox0.b0_spi_active_state_set
	_speed_get = libbox0.b0_spi_speed_get
	_speed_set = libbox0.b0_spi_speed_set

	_master_start = libbox0.b0_spi_master_start
	_master_stop = libbox0.b0_spi_master_stop

	_master_hd_write = libbox0.b0_spi_master_hd_write
	_master_hd_read = libbox0.b0_spi_master_hd_read
	_master_fd = libbox0.b0_spi_master_fd

	ss_count = None
	"""Number of slave select pins"""

	label = None
	"""String related to module
		Attributes:
		`self.label.pin`: Names of slave select pin
		`self.label.sclk`: SCLK pin
		`self.label.miso`: MISO pin
		`self.label.mosi`: MOSI pin
	"""

	ref = None
	"""Reference.
		attributes:
		`high`: HIGH_VALUE
		`low`: LOW_VALUE
		`type`: TYPE_OF_REFERENCE
	"""

	bitsize = None
	"""Supported bitsize"""

	speed = None
	"""Supported speeds"""

	def __init__(self, dev, index):
		ModuleInstance.__init__(self, dev, index, "b0_spi**")
		self.ss_count = self._pointer.ss_count
		self.label = object()
		self.label.sclk = string_converter(self._pointer.label.sclk)
		self.label.mosi = string_converter(self._pointer.label.mosi)
		self.label.miso = string_converter(self._pointer.label.miso)
		self.label.ss = string_array_converter(self._pointer.label.ss, self._pointer.ss_count)
		self.bitsize = cast_to_array("unsigned int", self._pointer.bitsize)
		self.speed = cast_to_array("unsigned long", self._pointer.speed)
		self.ref = self._pointer.ref

	def active_state_set(self, ss, value):
		ResultException.act(self._active_state_set(self._pointer, ss, value))

	def active_state_get(self, ss):
		value = ffi.new("bool")
		ResultException.act(self._active_state_get(self._pointer, ss, value))
		return (value[0] != 0)

	def master_start(self, tasks):
		failed_task_index = ffi.new("int *")
		failed_task_count = ffi.new("int *")
		ResultException.act(self._master_start(self._pointer, _to_ctasks(tasks), \
			failed_task_index, failed_task_count))
		return failed_task_index[0], failed_task_count[0]

	def master_stop(self):
		ResultException.act(self._master_stop(self._pointer))

	def master_hd_write(self, arg, data):
		arg = _to_sugar_arg(arg)
		data_buf = ffi.cast("void *", data.ctypes.data)
		ResultException.act(self._master_hd_write(self._pointer, arg, \
			data_buf, len(data)))

	def master_hd_read(self, arg, data):
		arg = _to_sugar_arg(arg)
		data_buf = ffi.cast("void *", data.ctypes.data)
		ResultException.act(self._master_hd_read(self._pointer, arg, data_buf, \
			len(data)))

	def master_fd(self, arg, write, read=None, count=None):
		"""
		write and write buffer
		"""
		if read is None:
			read = np.empty(len(write), dtype=write.dtype)

		if count is None:
			count = min(len(write), len(read))

		arg = _to_sugar_arg(arg)
		write_buf = ffi.cast("void *", write.ctypes.data)
		read_buf = ffi.cast("void *", read.ctypes.data)
		ResultException.act(self._fd(self._pointer, arg, write_buf, read_buf, count))
		return read

	def slave(self, addr, **kwargs):
		"""
		construct a Slave Object
		modX.slave(addr, ...) => Slave(addr, modX, ...)
		"""
		return Slave(addr, self, **kwargs)

	speed_set = speed_set
	speed_get = speed_get
