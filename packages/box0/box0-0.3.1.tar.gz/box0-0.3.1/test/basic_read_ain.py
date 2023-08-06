import box0
import sys
import numpy as np

dev = box0.usb.open_supported()
ain0 = dev.ain(0)

print("label")
i = 0
for l in ain0.label.chan:
	print(str(i) + l)
	i += 1

print("reference")
print("  high: %.3f" % ain0.ref.high)
print("  low: %.3f" % ain0.ref.low)

print("snapshot (bitsize, first-speed)")
for b in ain0.snapshot: print(str(b.bitsize), str(b.speed[0]))

print("count %i"%ain0.chan_count)

ain0.snapshot_prepare()

ain0.bitsize_speed_set(12, 100)
data = np.empty(10, dtype=np.float64)
ain0.snapshot_start(data)
print(data)

ain0.close()
dev.close()
