import box0
import numpy

# find thing to work with
dev = box0.usb.open_supported()
ain0 = dev.ain()
ain0.snapshot_prepare() # prepare for snapshot mode (ie snapshot of signal)

# do the work
values = numpy.empty(100, dtype=numpy.float32) # count=100, can vary though
ain0.snapshot_start(values) # blocking method (till data not readed)
print(values)

# dispose resources
ain0.close()
dev.close()
