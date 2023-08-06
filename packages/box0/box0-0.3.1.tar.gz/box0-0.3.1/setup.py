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

from setuptools import setup, find_packages
import os, io, re
import box0

# https://python-packaging-user-guide.readthedocs.io/single_source_version/

def read(*names, **kwargs):
	path = os.path.join(os.path.dirname(__file__), *names)
	encoding = kwargs.get("encoding", "utf8")
	with io.open(path, encoding=encoding) as fp:
		return fp.read()


def find_version(*file_paths):
	version_file = read(*file_paths)
	version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
							version_file, re.M)
	if version_match:
		return version_match.group(1)
	raise RuntimeError("Unable to find version string.")

setup(
	name = "box0",
	version = find_version("box0", "__init__.py"),
	author = "Kuldeep Singh Dhaka",
	author_email = "kuldeep@madresistor.com",
	description = ("libbox0 Binding"),
	license = "GPLv3+",
	keywords = "box0 libbox0 daq",
	url = "https://www.madresistor.com/box0",
	long_description = read('README'),
	long_description_content_type = 'text/markdown',
	packages = find_packages(include='box0.*'),
	install_requires = ["cffi>=1.0.0", "numpy>=1.11.0"],
	classifiers = [
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Topic :: Scientific/Engineering'
	]
)

