import threading
from hcsr04sensor.sensor import Measurement
import Queue

from sklearn.ensemble import ExtraTreesClassifier
import numpy as np

import datetime

import sys



#sensor = Measurement(trig_pin=19, echo_pin=26)

class Ultrasound_sensors(threading.Thread):
    
    def __init__(self, trig_pin1, echo_pin1, trig_pin2, echo_pin2, out_queue, sample_size, sample_wait, predict_size):
        
        threading.Thread.__init__(self)
        
        self._trig_pin1 = trig_pin1
        self._echo_pin1 = echo_pin1
        
        self._trig_pin2 = trig_pin2
        self._echo_pin2 = echo_pin2
        
        self._queue = out_queue
        self._iq = Queue.Queue() #internal Queue
        
        self._sensor1 = Measurement(trig_pin1, echo_pin1)
        self._sensor2 = Measurement(trig_pin2, echo_pin2)
        
        self._sample_size = sample_size
        self._sample_wait = sample_wait
        
        self._model = ExtraTreesClassifier(n_estimators=1000, max_depth=3)
        
        self._dt = datetime.datetime
        self._td = datetime.timedelta
        
        self._NO_PASSED = 0
        self._PASSED_1_TO_2 = 1
        self._PASSED_2_TO_1 = 2
        
        self._predict_size = predict_size
        
        
    def run(self):
        
        dist_diff = []
        i = 0
        pred_value = 0
        
        while(i < 1000):
            dist1 = self._sensor1.raw_distance(self._sample_size, self._sample_wait)
            dist2 = self._sensor2.raw_distance(self._sample_size, self._sample_wait)
            
            dist_diff.append((dist1 - dist2)//1)
            
            if len(dist_diff) == self._predict_size:
                pred_value = self._model.predict(np.array([dist_diff]))[0]
            
                if pred_value >= self._PASSED_1_TO_2:
                    cdt = datetime.datetime.now()
                    self._queue.put([pred_value]) #[cdt.year, cdt.month, cdt.day, cdt.weekday(), cdt.hour, cdt.minute//10, pred_value])
                
                dist_diff = []
                print "predicted direction: ", pred_value
                    
            i += 1
            
        return
        
    def _get_training_values(self, train_num):
        
        dist_diff = []
        y = []
        i = 0
        
        print "Start triggering sensors in a pattern chosen by you..."
        
        while(i < train_num):
            dist1 = self._sensor1.raw_distance(self._sample_size, self._sample_wait)
            dist2 = self._sensor2.raw_distance(self._sample_size, self._sample_wait)
            
            dist_diff.append((dist1 - dist2)//1)
            i += 1
    
        return dist_diff
    
    
    def train(self, train_num, divisor):
        
        dist_diff = self._get_training_values(train_num)
        dist_diff_p = [] #partial
        X_train = []
        y = []
        
        while(len(dist_diff) > 0):
            
            print "length dist_diff: ", len(dist_diff)
            dist_diff_p = dist_diff[0:divisor]
            
            
            print "Which direction is the person moving in?\n (0 = no sensor triggered)\n (1 = from sensor1 to sensor2),\n (2 = from sensor2 to sensor1)"
            print "Tree values depicting the difference of sensor1 - sensor2 in a row: ", dist_diff_p
            
            y.append(sys.stdin.read(2)[0])
            
            X_train.append(dist_diff_p)
            
            del dist_diff[0:divisor]
            
        self._model.fit(X_train, y)
                    
        return
