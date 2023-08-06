import box0

dev = box0.usb.open_supported()
ain = dev.ain()
aout = dev.aout()

ain.stream_prepare()
aout.stream_prepare()

box0.usb.aout_stream_pending(aout, 16*1024)
print("aout_stream_pending: OK")

box0.usb.ain_stream_delay(ain, 30)
print("ain_stream_delay: OK")

box0.usb.device_ctrlreq_timeout(dev, 100)
print("device_ctrlreq_timeout: OK")

box0.usb.device_bulk_timeout(dev, 100)
print("device_bulk_timeout: OK")

print("libusb_device_handle: ", box0.usb.libusb_device_handle(dev))
print("libusb_device: ", box0.usb.libusb_device(dev))
print("libusb_context: ", box0.usb.libusb_context(dev))

ain.close()
aout.close()
dev.close()
