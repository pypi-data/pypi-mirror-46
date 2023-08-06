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

from box0._binding import libbox0, ffi
from box0.exceptions import ResultException
from box0.device import Device
from box0.module import Ain, Aout
from box0.misc.box0v5.ps import Box0V5PowerSupply

_open_vid_pid = libbox0.b0_usb_open_vid_pid
_open_supported = libbox0.b0_usb_open_supported

class UsbAin(Ain):
	_stream_delay = libbox0.b0_usb_ain_stream_delay

	def stream_delay(self, delay):
		"""
		Set AIN callback delay.
		Decreasing the value will increase the update rate.

		:param int ms_delay: Delay (in milliseconds)

		.. warning::

			The already set value may be platform dependent.
			Modify at your own risk.

		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._stream_delay(self._pointer, delay))

class UsbAout(Aout):
	_stream_pending = libbox0.b0_usb_aout_stream_pending

	def stream_pending(self, pending):
		"""
		Set AOUT maximum data (in bytes) that can be pending at kernel.

		:param int pending: pending memory (bytes)

		.. warning::

			The already set value may be platform dependent.
			Modify at your own risk.

		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._stream_pending(self._pointer, pending))

class UsbDevice(Device):
	_bulk_timeout = libbox0.b0_usb_device_bulk_timeout
	_ctrlreq_timeout = libbox0.b0_usb_device_ctrlreq_timeout

	_libusb_context = libbox0.b0_usb_libusb_context
	_libusb_device = libbox0.b0_usb_libusb_device
	_libusb_device_handle = libbox0.b0_usb_libusb_device_handle

	def libusb_context(self):
		"""
		Get libusb context pointer

		:return: Pointer to `libusb_context` (python-cffi)
		"""
		ptr = ffi.new("libusb_device_handle **")
		ResultException.act(self._libusb_context(self._pointer, ptr))
		return ptr[0]

	def libusb_device(self):
		"""
		Get libusb device pointer

		:return: Pointer to `libusb_device_handle` (python-cffi)
		"""
		ptr = ffi.new("libusb_device **")
		ResultException.act(self._libusb_device(self._pointer, ptr))
		return ptr[0]

	def libusb_device_handle(self):
		"""
		Get libusb device handle pointer

		:return: Pointer to `libusb_device_handle` (python-cffi)
		"""
		ptr = ffi.new("libusb_device_handle **")
		ResultException.act(self._libusb_device_handle(self._pointer, ptr))
		return ptr[0]

	def bulk_timeout(dev, timeout):
		"""
		Set USB bulk transfer timeout

		:param int timeout: Timeout in milliseconds

		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._bulk_timeout(self._pointer, timeout))

	def ctrlreq_timeout(dev, timeout):
		"""
		Set USB control request timeout

		:param int timeout: Timeout in milliseconds

		:raises ResultException: if libbox0 return negative result code
		"""
		ResultException.act(self._ctrlreq_timeout(self._pointer, timeout))

	def ain(self, index = 0):
		# Plug-in the USB specfic AIN
		return UsbAin(self, index)

	def aout(self, index = 0):
		# Plug-in the USB specfic AOUT
		return UsbAout(self, index)

class Box0V5UsbDevice(UsbDevice, Box0V5PowerSupply):
	pass

def convert_to_device(dev):
	if libbox0.b0v5_valid_test(dev) == libbox0.B0_OK:
		"""box0-v5 has some extra device specific functionality"""
		return Box0V5UsbDevice(dev)

	return UsbDevice(dev)

def open_supported():
	"""
	Open any supported device
	return None if none is found

	:raises ResultException: if libbox0 return negative result code
	"""
	dev_ptr = ffi.new("b0_device **")
	ResultException.act(_open_supported(dev_ptr))
	return convert_to_device(dev_ptr[0])

def open_vid_pid(vid, pid):
	"""
	Open a device using vid, pid

	:raises ResultException: if libbox0 return negative result code
	"""
	dev_ptr = ffi.new("b0_device **")
	ResultException.act(_open_vid_pid(dev_ptr, vid, pid))
	return convert_to_device(dev_ptr[0])
