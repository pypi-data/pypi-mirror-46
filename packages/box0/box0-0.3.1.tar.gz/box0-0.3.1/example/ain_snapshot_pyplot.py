import box0
import time
import numpy as np
from pylab import *

SAMPLE_SPEED = 100000
SAMPLE_COUNT = 500
BITSIZE = 12

dev = box0.usb.open_supported()
ain0 = dev.ain(0)
ain0.snapshot_prepare()

xlabel('time (s)')
ylabel('voltage (V)')
title('About as simple as it gets, folks')
grid(True)

ain0.bitsize_speed_set(BITSIZE, SAMPLE_SPEED)
s = np.empty(int(SAMPLE_COUNT), dtype=np.float64)
ain0.snapshot_start(s)

t = arange(0.0, SAMPLE_COUNT / float(SAMPLE_SPEED), 1 / float(SAMPLE_SPEED))
clf()
grid(True)

print("s is" + str(s))
print("t is" + str(t))

plot(t, s, 'r.-')

savefig("test.png")

ain0.close()
dev.close()

show()
