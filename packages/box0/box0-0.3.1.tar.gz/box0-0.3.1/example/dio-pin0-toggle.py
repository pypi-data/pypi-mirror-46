import box0
import time

dev = box0.usb.open_supported()
dio0 = dev.dio()
dio0.basic_prepare()

#note: connect LED on "0" pin of "DIO0"
pin0 = dio0.pin(0)
pin0.output()
pin0.high()
pin0.enable()

dio0.basic_start()

while True:
	try:
		pin0.toggle()
		time.sleep(0.1)
	except KeyboardInterrupt:
		break

dio0.basic_stop()

dio0.close()
dev.close()
