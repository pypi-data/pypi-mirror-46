import box0
import time

dev = box0.usb.open_supported()

dio0 = dev.dio(0)

dio0.basic_prepare()

pin0 = dio0.pin(0)

pin0.output()
pin0.low()
pin0.hiz = dio0.DISABLE

dio0.basic_start()

try:
	while True:
		pin0.toggle()
		time.sleep(0.5)
except KeyboardInterrupt:
	print("Bye bye")

pin0.low()
pin0.hiz = dio0.ENABLE

dio0.basic_stop()
dio0.close()

dev.close()
