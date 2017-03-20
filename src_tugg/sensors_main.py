import ultrasound_sensors as uss

import Queue as Q

q = Q.Queue()

sensors = uss.Ultrasound_sensors(19, 26, 6, 13, q, sample_size=1, sample_wait=0.06, predict_size=6)

sensors.train(train_num=102, divisor=6)

print "Starting sensors thread..."

sensors.start()
