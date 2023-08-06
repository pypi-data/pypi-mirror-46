import box0
import numpy

dev = box0.usb.open_supported()
i2c = dev.i2c()
i2c.master_prepare()

w = numpy.array([0x78], dtype=numpy.uint8)
r = numpy.array([0x45], dtype=numpy.uint8)

i2c.master_start([{
	'addr': 0x77,
	'data': w,
	'flags': 'write'
}, {
	'addr': 0x77,
	'data': r,
	'flags': 'read'
}])

print('w[0]', hex(w[0]))
print('r[0]', hex(r[0]))
