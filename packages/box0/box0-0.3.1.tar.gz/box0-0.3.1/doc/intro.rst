Introduction to pyBox0
======================

pyBox0 is a Python binding of `libbox0`_.
`libbox0`_ is the C library that does the communication with physical devices.

.. image:: img/box0-infra.svg.png
   :alt: Box0 infrastructure

Importing
---------

.. code:: python

	import box0

What is a Device
----------------

A device is an interface to the physical device you have.

A device can be acquired via multiple method, at the moment USB only.

Opening a device
----------------

.. code-block:: python

	import box0

	dev = box0.usb.open_supported()
	# ... do something with "dev"

In the above code, :class:`box0.usb.open_supported` try to open any USB device
connected that can be used as Box0. quick and easy!

You can do something with "dev" like

.. code-block:: python

	import box0

	dev = box0.usb.open_supported()
	print(dev.name) # Print device name (provided by device - brand)
	print(dev.serial) # Print serial number (provided by device)
	print(dev.manuf) # Print manufacturer name (provided by device)

What is a Module
----------------

A module is a portion of device that perform a dedicated function.
A device can contain multiple modules.

Example of module with their uses.

  ================================= ==========   =================================================================================================
  Name of module                    Short name   Use
  ================================= ==========   =================================================================================================
  Analog In                          AIN         Read `analog signal <https://en.wikipedia.org/wiki/Analog_signal>`__
  Analog Out                         AOUT        Generate `analog signal <https://en.wikipedia.org/wiki/Analog_signal>`__
  Digital Input/Output               DIO         Generate, Read `digital signal <https://en.wikipedia.org/wiki/Digital_signal_(electronics)>`__
  Serial Peripherial Interface       SPI         Communicate with `SPI <https://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus>`__ slaves
  Inter Integerated Communication   I2C          Communicate with `I2C <https://en.wikipedia.org/wiki/I%C2%B2C>`__ slaves
  Pulse Width Modulation             PWM         Generate `Pulse Width Modulation <https://en.wikipedia.org/wiki/Pulse-width_modulation>`__
  ================================= ==========   =================================================================================================

Opening a module
----------------

From the above, we know how to open a device.
Now, we will open a module from device.

.. code-block:: python

	import box0

	dev = box0.usb.open_supported()

	my_ain = dev.ain() # Open Analog In (with index=0) from device

	# .... do something with "my_ain"

The above pattern can be applied for all type of module.

 ===========   ========================
 Short name    <method>
 ===========   ========================
  AIN           :func:`box0.Device.ain`
  AOUT          :func:`box0.Device.aout`
  DIO           :func:`box0.Device.dio`
  SPI           :func:`box0.Device.spi`
  I2C           :func:`box0.Device.i2c`
  PWM           :func:`box0.Device.pwm`
 ===========   ========================

You can use ``my_module = dev.<method>()``.

Exception and failure
----------------------

`libbox0`_. functions return a negative integer value (actually enum)
to tell that some kind of error has occured.

pyBox0 convert these negative values to Exception with the help of a exception class :class:`box0.ResultException`

.. code-block:: python

	import box0

	try:
		dev = box0.usb.open_supported()
	except ResultException, e:
		print("failed! (%s)" % e)
		# name of the exception: e.name()
		# explaination of exception: e.explain()

.. _libbox0: http://gitlab.com/madresistor/libbox0

Resource management
--------------------

Device, resource and driver are resources which are taken for a time and
returned back when it is no more required.

A device, module and driver after closing cannot be used.
Doing so will result in undefined behaviour.
You can use ``close()`` method for closing, the ``del`` keyword leads to ``close()`` too.

You can also use ``with`` keyword for automatic disposal when execution of a block finishes.
Device, module and driver support ``with`` statement.
