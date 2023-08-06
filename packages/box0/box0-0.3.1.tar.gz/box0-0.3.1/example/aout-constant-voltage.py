import box0
import numpy

CONSTANT_VOLTAGE = 1.5

dev = box0.usb.open_supported()
aout0 = dev.aout()

aout0.snapshot_prepare()
values = numpy.array([CONSTANT_VOLTAGE], dtype=numpy.float32)
aout0.snapshot_start(values) # non-blocking, return right after operation

input("Press Enter to exit")

aout0.snapshot_stop()
aout0.close()
dev.close()
