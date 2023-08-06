import numpy
import box0

dev = box0.usb.open_supported()
spi = dev.spi()
spi.master_prepare()

w = numpy.array([12,67,90], dtype=numpy.uint8)
r = numpy.array([0, 0, 0], dtype=numpy.uint8)

spi.master_start({
	'addr': 0,
	'bitsize': 8,
	'flags': ('mode0', ),
	'write': w,
	'read': r
})

print('w[0:3]', w[0:3])
print('r[0:3]', r[0:3])
print('SUCCESS', w[0:3] == r[0:3])
