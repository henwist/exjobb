import threading
from hcsr04sensor.sensor import Measurement
import Queue

queue = Queue.Queue()
condition = threading.Condition()

import spidev
spidev = spidev.SpiDev()
spidev.open(0,0)
import leddisplay
dis = leddisplay.Leddisplay(name='display',
			  spidev=spidev,
			queue=queue,
			condition=condition,
			 sleep_between_digits_ms=1000, 
			clear_display_after_ms=2000)



dis.start()



sensor = Measurement(trig_pin=19, echo_pin=26)

queue.put(123)
queue.put(456.789)
queue.put('None') #None will finish the thread's execution

with condition:
	condition.notify()

i=100
while(i > 0):
	print "distance: ", sensor.raw_distance(sample_size=1, sample_wait=0.06)
	i -= 1

dis.join()
