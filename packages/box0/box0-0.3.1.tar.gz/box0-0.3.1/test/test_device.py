import box0

dev = box0.usb.open_supported()
print("Name: " + dev.name)
print("Serial: " + dev.serial)
print("Manuf: " + dev.manuf)
dev.close()
print("bye bye...")
