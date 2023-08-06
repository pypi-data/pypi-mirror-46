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

from box0.device import Device
from box0.backend import usb
from box0.exceptions import ResultException
from box0.extra import Version, RefType
import box0.module as module
import box0.driver as driver

__all__ = ["Device", "ResultException", "usb", "Version", "RefType", "module",
				"driver"]
__version__ = '0.3.1'
__author__ = 'Kuldeep Singh Dhaka <kuldeep@madresistor.com>'
__licence__ = 'GNU General Public License v3 or later (GPLv3+)'
