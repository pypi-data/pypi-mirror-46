import box0
import time

dev = box0.usb.open_supported()
pwm = dev.pwm(0)

bitsize = pwm.bitsize[0]
speed, period = pwm.output_calc(bitsize, 1)

print("speed: ", speed)
print("period: ", period)

pwm.output_prepare()
pwm.speed_set(speed)
pwm.period_set(period)
pwm.width_set(0, pwm.output_calc_width(period, 50))
pwm.output_start()

for l in pwm.label.pin:
	print("label: " + l)

for b in pwm.bitsize:
	print("bitsize: " + str(b))

while True:
	time.sleep(.5)

pwm.output_stop()
pwm.close()
dev.close()
