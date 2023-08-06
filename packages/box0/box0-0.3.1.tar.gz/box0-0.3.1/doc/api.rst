The pyBox0 API Reference
************************

The "box0" module
=================

.. automodule:: box0

Device
^^^^^^

.. autoclass:: box0.Device
   :members:
   :member-order: bysource
   :exclude-members: name, manuf, serial, modules

   .. autoattribute:: name
      :annotation:
   .. autoattribute:: manuf
      :annotation:
   .. autoattribute:: serial
      :annotation:
   .. autoattribute:: modules
      :annotation:

ResultException
^^^^^^^^^^^^^^^

.. autoexception:: box0.ResultException
   :members:
   :member-order: bysource
   :exclude-members: act

Version
^^^^^^^

.. autoclass:: box0.Version
   :members:
   :member-order: bysource
   :exclude-members: code, major, minor, patch

   .. autoattribute:: code
      :annotation:
   .. autoattribute:: major
      :annotation:
   .. autoattribute:: minor
      :annotation:
   .. autoattribute:: patch
      :annotation:

The "module" module
===================

.. automodule:: box0.module

Module
^^^^^^

.. autoclass:: box0.module.Module
   :members:
   :member-order: bysource
   :inherited-members:
   :exclude-members: index, type, name

   .. autoattribute:: index
      :annotation:
   .. autoattribute:: type
      :annotation:
   .. autoattribute:: name
      :annotation:

Analog In
^^^^^^^^^

.. autoclass:: box0.module.Ain
   :members:
   :member-order: bysource
   :inherited-members:
   :exclude-members: chan_count, buffer_size, capab, label, ref, stream, snapshot

   .. autoattribute:: chan_count
      :annotation:
   .. autoattribute:: buffer_size
      :annotation:
   .. autoattribute:: capab
      :annotation:
   .. autoattribute:: label
      :annotation:
   .. autoattribute:: ref
      :annotation:
   .. autoattribute:: stream
      :annotation:
   .. autoattribute:: snapshot
      :annotation:

Analog Out
^^^^^^^^^^

.. autoclass:: box0.module.Aout
   :members:
   :member-order: bysource
   :exclude-members: chan_count, buffer_size, capab, label, ref, stream, snapshot

   .. autoattribute:: chan_count
      :annotation:
   .. autoattribute:: buffer_size
      :annotation:
   .. autoattribute:: capab
      :annotation:
   .. autoattribute:: label
      :annotation:
   .. autoattribute:: ref
      :annotation:
   .. autoattribute:: stream
      :annotation:
   .. autoattribute:: snapshot
      :annotation:

Digital Input/Output
^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: box0.module.dio.Pin
   :members:
   :member-order: bysource

.. autoclass:: box0.module.Dio
   :members:
   :member-order: bysource
   :exclude-members: pin_count, capab, label, ref

   .. autoattribute:: pin_count
      :annotation:
   .. autoattribute:: capab
      :annotation:
   .. autoattribute:: label
      :annotation:
   .. autoattribute:: ref
      :annotation:

Pulse Width Modulation
^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: box0.module.Pwm
   :members:
   :member-order: bysource
   :exclude-members: pin_count, label, ref, bitsize, speed

   .. autoattribute:: pin_count
      :annotation:
   .. autoattribute:: label
      :annotation:
   .. autoattribute:: ref
      :annotation:
   .. autoattribute:: bitsize
      :annotation:
   .. autoattribute:: speed
      :annotation:

Inter Integerated Communication
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: box0.module.i2c.Slave
   :members:
   :member-order: bysource

.. autoclass:: box0.module.I2c
   :members:
   :member-order: bysource
   :exclude-members: label, ref, version

   .. autoattribute:: label
      :annotation:
   .. autoattribute:: ref
      :annotation:
   .. autoattribute:: version
      :annotation:

Serial Peripherial Interface
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: box0.module.spi.Slave
   :members:
   :member-order: bysource

.. autoclass:: box0.module.Spi
   :members:
   :member-order: bysource
   :exclude-members: ss_count, label, ref, bitsize, speed

   .. autoattribute:: ss_count
      :annotation:
   .. autoattribute:: label
      :annotation:
   .. autoattribute:: ref
      :annotation:
   .. autoattribute:: bitsize
      :annotation:
   .. autoattribute:: speed
      :annotation:

The "usb" backend
=================

.. automodule:: box0.backend.usb
  :members:
  :member-order: bysource

.. autoclass:: box0.backend.usb.UsbAin
  :members:
  :member-order: bysource

.. autoclass:: box0.backend.usb.UsbAout
  :members:
  :member-order: bysource

.. autoclass:: box0.backend.usb.UsbDevice
  :members:
  :member-order: bysource

.. autoclass:: box0.backend.usb.Box0V5UsbDevice
  :members:
  :member-order: bysource

The "box0v5" (box0-v5)
======================

.. autoexception:: box0.misc.box0v5.ps.Box0V5PowerSupply
   :members:
   :member-order: bysource

The "driver" module
====================

.. autoclass:: box0.driver.driver.Driver
   :members:
   :member-order: bysource

.. autoclass:: box0.driver.Ads1220
   :members:
   :member-order: bysource

.. autoclass:: box0.driver.Adxl345
   :members:
   :member-order: bysource

.. autoclass:: box0.driver.HBridge
   :members:
   :member-order: bysource

.. autoclass:: box0.driver.Mcp342x
   :members:
   :member-order: bysource
