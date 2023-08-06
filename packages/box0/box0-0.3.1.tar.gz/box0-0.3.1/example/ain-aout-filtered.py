import time
import box0
import numpy as np
from scipy import signal

raise Exception("TODO: NEED TO BE CODED")

##filtering
## http://stackoverflow.com/a/13740532
niqFreq = sv.speed / 2.0
cutoff = 100.0 # Hz
Wn = cutoff / niqFreq
order = 3
print("niqFreq:", niqFreq)
print("cutoff:", cutoff)
print("order:", order)
print("Wn:", Wn)
b, a = signal.butter(order, Wn, 'low')

#filtering
	#~ global a, b
	#~ y = signal.filtfilt(b, a, y)

dev = box0.usb.open_supported()
ain = dev.ain(0)
aout = dev.aout(0)

speed = 10000
bitsize = 12

ain.stream_prepare()
aout.stream_prepare()

ain.bitsize_speed_set(bitsize, speed)
aout.bitsize_speed_set(bitsize, speed)

ain.stream_start()
aout.stream_start()

try:
	count = speed / 10
	data = np.empty(count)
	while(True):
		ain.stream_read(data)
		aout.stream_write(data)
except:
	# no problem
	pass

ain.stream_stop()
aout.stream_stop()

ain.close()
aout.close()
dev.close()
