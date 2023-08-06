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

from box0._binding import ffi, libbox0, string_converter, cast_to_array, DummyObject
from box0.exceptions import ResultException
from box0.module import ModuleInstance
import numpy as np

class Slave(object):
	def __init__(self, addr, mod, version=None):
		self.addr = addr
		self.mod = mod
		self._arg = ffi.new("b0_i2c_sugar_arg *", {
			'addr': addr,
			'version': I2c.SM if version is None else version
		})

	def detect(self):
		return self.mod.master_slave_detect(self._arg)

	def read(self, read):
		return self.mod.master_read(self._arg, read)

	def write(self, write):
		return self.mod.master_write(self._arg, write)

	def write8_read(self, write_byte, read):
		return self.mod.master_write8_read(self._arg, write_byte, read)

	def write_read(self, write, read):
		return self.mod.master_write_read(self._arg, write, read)

	def __str__(self):
		return "Slave Address: " + hex(self.addr)

def _task_cflags(task):
	"""
	Convert the task flags to C flags
	"""
	_flags = 0

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
		if flag.lower() is 'last':
			raise Exception("LAST flag is automatically infered")

		_flag = {
			'write': libbox0.B0_I2C_TASK_WRITE,
			'w': libbox0.B0_I2C_TASK_WRITE,
			'read': libbox0.B0_I2C_TASK_READ,
			'r': libbox0.B0_I2C_TASK_READ
		}.get(flag.lower())

		if _flag is None: raise Exception("Invalid flag %s" % flag)
		_flags |= _flag

	return _flags

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
		version = task['version'] if 'version' in task else I2c.SM
		_tasks.append({
			'flags': _task_cflags(task),
			'addr': task['addr'],
				'version': version,
			'data': ffi.cast("void *", task['data'].ctypes.data),
			'count': task['data'].nbytes
		})

	_tasks[-1]['flags'] |= libbox0.B0_I2C_TASK_LAST
	return ffi.new("b0_i2c_task []", _tasks)

def to_sugar_arg(arg):
	if type(arg) is dict:
		return ffi.new("b0_i2c_sugar_arg *", arg)
	elif type(arg) is int:
		return ffi.new("b0_i2c_sugar_arg *", {
			'addr': arg,
			'version': I2c.SM
		})
	return arg

class I2c(ModuleInstance):
	_open = libbox0.b0_i2c_open
	_close = libbox0.b0_i2c_close

	_master_prepare = libbox0.b0_i2c_master_prepare
	_master_start = libbox0.b0_i2c_master_start
	_master_stop = libbox0.b0_i2c_master_stop
	_master_read = libbox0.b0_i2c_master_read
	_master_write = libbox0.b0_i2c_master_write
	_master_write8_read = libbox0.b0_i2c_master_write8_read
	_master_write_read = libbox0.b0_i2c_master_write_read
	_master_slave_id = libbox0.b0_i2c_master_slave_id
	_master_slave_detect = libbox0.b0_i2c_master_slave_detect
	_master_slaves_detect = libbox0.b0_i2c_master_slaves_detect

	SM = libbox0.B0_I2C_VERSION_SM
	FM = libbox0.B0_I2C_VERSION_FM
	HS = libbox0.B0_I2C_VERSION_HS
	HS_CLEANUP1= libbox0.B0_I2C_VERSION_HS_CLEANUP1
	FMPLUS = libbox0.B0_I2C_VERSION_FMPLUS
	UFM = libbox0.B0_I2C_VERSION_UFM
	VER5 = libbox0.B0_I2C_VERSION_VER5
	VER6 = libbox0.B0_I2C_VERSION_VER6

	label = None
	"""String related to module.
		Attributes:
		`self.label.sck`: SCK pin
		`self.label.sck`: SCL pin
	"""

	ref = None
	"""Reference.
		attributes:
		`high`: HIGH_VALUE
		`low`: LOW_VALUE
	"""

	version = None
	"""I2C versions supported"""

	def __init__(self, dev, index):
		ModuleInstance.__init__(self, dev, index, "b0_i2c**")
		self.label = DummyObject()
		self.label.sck = string_converter(self._pointer.label.sck)
		self.label.sda = string_converter(self._pointer.label.sda)
		self.version = cast_to_array("b0_i2c_version", self._pointer.version)
		self.ref = self._pointer.ref

	def master_prepare(self):
		"""
		Prepare for master mode

		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._master_prepare(self._pointer))

	def master_start(self):
		"""
		Start in master mode

		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._master_start(self._pointer))

	def master_slave_id(self, arg):
		"""
		return (manufacturer, part, revision)
		"""
		manuf = ffi.new("uint16_t*")
		part = ffi.new("uint16_t*")
		rev = ffi.new("uint8_t*")
		ResultException.act(self._master_slave_id(self._pointer, arg, manuf, part, rev))
		return manuf[0], part[0], rev[0]

	def master_start(self, tasks):
		"""
		tasks to execute
		"""
		failed_task_index = ffi.new("int *")
		failed_task_ack = ffi.new("int *")
		ResultException.act(self._master_start(self._pointer, _to_ctasks(tasks), \
			failed_task_index, failed_task_ack))
		return failed_task_index[0], failed_task_ack[0]

	def master_stop(self):
		ResultException.act(self._master_stop(self._pointer))

	def master_slave_detect(self, arg):
		arg = to_sugar_arg(arg)
		detected = ffi.new("bool*")
		ResultException.act(self._master_slave_detect(self._pointer, arg, detected))
		return (detected[0] != 0)

	def master_slaves_detect(self, version, addresses):
		addr_array = ffi.new("uint8_t []", addresses)
		det_array = ffi.new("bool []", len(addresses))
		processed = ffi.new("size_t *")
		ResultException.act(self._master_slaves_detect(self._pointer, version, \
				addr_array, det_array, len(addresses), processed))
		return [det_array[0]!=0 for i in range(processed[0])]

	def master_write8_read(self, arg, write_byte, read):
		"""
		read can be a number [no of bytes to read]
		or a numpy array, that contain no of bytes to read

		return the readed array
		"""
		arg = to_sugar_arg(arg)
		if not isinstance(read, np.ndarray):
			read = int(read)
			assert (read > 0)
			read = np.empty(read, dtype=np.uint8)

		read_buf = ffi.cast("void *", read.ctypes.data)
		ResultException.act(self._master_write8_read(self._pointer, arg, \
					write_byte, read_buf, read.nbytes))
		return read

	def master_write_read(self, arg, write, read):
		"""
		first write buffer and then read
		return the readed array
		"""
		arg = to_sugar_arg(arg)
		if not isinstance(read, np.ndarray):
			read = int(read)
			assert (read > 0)
			read = np.empty(read, dtype=np.uint8)

		write_buf = ffi.cast("void *", write.ctypes.data)
		read_buf = ffi.cast("void *", read.ctypes.data)
		ResultException.act(self._master_write8_read(self._pointer, arg, \
				write_buf, write.nbytes, read_buf, read.nbytes))
		return read

	def master_write(self, arg, write):
		"""
		`write' is assumed to be a numpy array
		"""
		arg = to_sugar_arg(arg)
		write_ptr = ffi.cast("void *", write.ctypes.data)
		result = self._master_write(self._pointer, arg, write_ptr, write.nbytes)
		ResultException.act(result)

	def master_read(self, arg, read):
		"""
		`read' can be a number [no of bytes to read] or a numpy array
		"""
		arg = to_sugar_arg(arg)
		if not isinstance(read, np.ndarray):
			read = int(read)
			assert (read > 0)
			read = np.empty(read, dtype=np.uint8)

		data_ptr = ffi.cast("void *", read.ctypes.data)
		result = self._master_read(self._pointer, arg, data_ptr, read.nbytes)
		ResultException.act(result)
		return read

	def slave(self, addr, **kwargs):
		"""
		construct a Slave Object
		modX.slave(addr, ...) => Slave(addr, modX, ...)
		"""
		return Slave(addr, self, **kwargs)
