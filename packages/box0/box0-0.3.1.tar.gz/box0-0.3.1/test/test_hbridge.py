import box0
import time

dev = box0.usb.open_supported()
dio = dev.dio()
dio.basic_prepare()
hbridge = box0.driver.HBridge(dio)

dio0.basic_start()

print("disable")
hbridge.disable()
time.sleep(1)

print("forward")
hbridge.forward()
time.sleep(1)

print("backward")
hbridge.backward()
time.sleep(1)

dio0.basic_stop()
hbridge.close()
dio.close()
dev.close()
