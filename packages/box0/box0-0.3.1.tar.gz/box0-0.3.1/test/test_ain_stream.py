import box0
import sys
import time
import numpy as np

dev = box0.usb.open_supported()
ain0 = dev.ain(0)

SPEED = 100
BITSIZE = 12

print("bitsize: %i" % BITSIZE)
print("speed: %i" % SPEED)

ain0.stream_prepare()
ain0.bitsize_speed_set(BITSIZE, SPEED)
ain0.stream_start()

try:
	arr = np.empty(SPEED / 10) # 100ms data
	while True:
		ain0.stream_read(arr)
		print(str(arr))
except:
	print("exiting...")

ain0.stream_stop()
ain0.close()
dev.close()
