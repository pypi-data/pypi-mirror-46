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

from box0._binding import ffi, libbox0, string_array_converter, \
							mode_bitsize_speeds, DummyObject
from box0.exceptions import ResultException
import numpy as np
from box0.module import ModuleInstance
from box0.module.module import bitsize_speed_set, \
							bitsize_speed_get, chan_seq_set, chan_seq_get

class Ain(ModuleInstance):
	"""
	.. uml::
	   [*] -d-> Opened : Ain()
	   Opened -d-> Closed : close()
	   Closed -d-> [*]

	   Opened -r-> Stream
	   Stream -l-> Opened

	   Opened -l-> Snapshot
	   Snapshot -r-> Opened

	   state Stream {
		  state "Running" as StreamRunning
		  state "Stopped" as StreamStopped

		  [*] -d-> StreamStopped : stream_prepare()

		  StreamStopped -u-> StreamRunning : stream_start()
		  StreamRunning -d-> StreamStopped : stream_stop()
		  StreamStopped --> [*]

		  StreamStopped -u-> StreamStopped : chan_seq_set(), bitsize_speed_set()

		  StreamRunning -u-> StreamRunning: stream_read()
	   }

	   state Snapshot {
		  state "Running" as SnapshotRunning
		  state "Stopped" as SnapshotStopped

		  [*] -d-> SnapshotStopped : snapshot_prepare()
		  SnapshotStopped -u-> SnapshotRunning : snapshot_start()
		  SnapshotRunning -d-> SnapshotStopped : snapshot_stop(), [Acquisition complete]
		  SnapshotStopped --> [*]

		  SnapshotStopped -u-> SnapshotStopped : bitsize_speed_set(), chan_seq_set()
	   }
	"""
	_open = libbox0.b0_ain_open
	_close = libbox0.b0_ain_close

	_bitsize_speed_set = libbox0.b0_ain_bitsize_speed_set
	_bitsize_speed_get = libbox0.b0_ain_bitsize_speed_get
	_chan_seq_set = libbox0.b0_ain_chan_seq_set
	_chan_seq_get = libbox0.b0_ain_chan_seq_get

	_stream_prepare = libbox0.b0_ain_stream_prepare
	_stream_start = libbox0.b0_ain_stream_start
	_stream_read = libbox0.b0_ain_stream_read
	_stream_read_double = libbox0.b0_ain_stream_read_double
	_stream_read_float = libbox0.b0_ain_stream_read_float
	_stream_stop = libbox0.b0_ain_stream_stop

	_snapshot_prepare = libbox0.b0_ain_snapshot_prepare
	_snapshot_start = libbox0.b0_ain_snapshot_start
	_snapshot_start_double = libbox0.b0_ain_snapshot_start_double
	_snapshot_start_float = libbox0.b0_ain_snapshot_start_float
	_snapshot_stop = libbox0.b0_ain_snapshot_stop

	chan_count = None
	"""Number of channels"""

	buffer_size = None
	"""Number of bytes available"""

	capab = None
	"""Capabilities mask"""

	label = None
	"""String related to module (Names of channel in `self.label.chan`)"""

	ref = None
	"""Reference. attributes `high: HIGH_VALUE, low: LOW_VALUE, type: TYPE_OF_REFERENCE`"""

	stream = None
	"""Stream mode list"""

	snapshot = None
	"""Snapshot mode list"""

	def __init__(self, dev, index):
		ModuleInstance.__init__(self, dev, index, "b0_ain**")
		self.chan_count = self._pointer.chan_count
		self.buffer_size = self._pointer.buffer_size
		self.capab = self._pointer.capab
		self.label = DummyObject()
		self.label.chan = string_array_converter(self._pointer.label.chan, \
								self._pointer.chan_count)
		self.ref = self._pointer.ref
		self.stream = mode_bitsize_speeds(self._pointer.stream)
		self.snapshot = mode_bitsize_speeds(self._pointer.snapshot)

	def snapshot_prepare(self):
		"""
		Prepare for Snapshot mode
		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._snapshot_prepare(self._pointer))

	def snapshot_start(self, data, count=None):
		"""
		Get data in snapshot mode

		:param numpy.ndarray data: NumPy array to store readed value
		:param int count: Number of samples to read (Only mandatory for data type Void)
		:raises ResultException: if libbox0 return negative result code

		.. warning::

			This function is blocking and will not return until acquire all data
		"""
		RAW = {'cast': 'void *', 'call': self._snapshot_start}
		sel = {
			np.void: RAW, np.int8: RAW, np.uint8: RAW, np.int16: RAW, np.uint16: RAW,
			np.int32: RAW, np.uint32: RAW, np.int64: RAW, np.uint64: RAW,
			np.float32: {'cast': 'float *', 'call': self._snapshot_start_float},
			np.float64: {'cast': 'double *', 'call': self._snapshot_start_double}
		}.get(np.obj2sctype(data.dtype))

		if sel is None:
			raise Exception("numpy memory type not supported")

		# Beware, we are not checking array overflow
		if count is None:
			if np.obj2sctype(data.dtype) is np.void:
				raise Exception("If data type is Void, count is mandatory")
			else:
				count = data.size

		data_ptr = ffi.cast(sel['cast'], data.ctypes.data)
		ResultException.act(sel['call'](self._pointer, data_ptr, count))

	def snapshot_stop(self):
		"""
		Stop an ongoing snapshot acquisition

		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._snapshot_stop(self._pointer))

	def stream_prepare(self):
		"""
		Prepare for streaming mode

		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._stream_prepare(self._pointer))

	def stream_start(self):
		"""
		Start streaming

		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._stream_start(self._pointer))


	def stream_read(self, data, count=None, allowPartial=False):
		"""
		Read data from stream

		:param numpy.ndarray data: Store readed data
		:param int count: Number of samples to read (Only mandatory for data type Void)
		:param bool allowPartial: if False, return only after reading total requested samples
		:rtype: int
		:return: number of samples readed

		:raises ResultException: if libbox0 return negative result code

		.. note::

			This function can work in two modes.

			blocking: if `allowPartial is False`, block until all data is readed

			non-blocking: if `allowPartial is True`, try to read as much as requested data and return
		"""
		RAW = {'cast' : 'void *', 'call': self._stream_read}
		sel = {
			np.void: RAW, np.int8: RAW, np.uint8: RAW, np.int16: RAW, np.uint16: RAW,
			np.int32: RAW, np.uint32: RAW, np.int64: RAW, np.uint64: RAW,
			np.float32: {'cast': 'float *', 'call': self._stream_read_float},
			np.float64: {'cast': 'double *', 'call': self._stream_read_double}
		}.get(np.obj2sctype(data.dtype))

		if sel is None:
			raise Exception("numpy memory type not supported, (hint: use numpy.void)")

		# Beware, we are not checking array overflow
		if count is None:
			if np.obj2sctype(data.dtype) is np.void:
				raise Exception("If data type is Void, count is mandatory")
			else:
				count = data.size

		data_ptr = ffi.cast(sel['cast'], data.ctypes.data)
		actual_readed = ffi.new("size_t *") if allowPartial else ffi.NULL
		ResultException.act(sel['call'](self._pointer, data_ptr, count, \
							actual_readed))
		return actual_readed[0] if allowPartial else count

	def stream_stop(self):
		"""
		Stop streaming

		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._stream_stop(self._pointer))

	# Reuse common part

	bitsize_speed_set = bitsize_speed_set
	bitsize_speed_get = bitsize_speed_get

	chan_seq_set = chan_seq_set
	chan_seq_get = chan_seq_get
