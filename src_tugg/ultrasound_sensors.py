import threading
from hcsr04sensor.sensor import Measurement
import Queue

from sklearn.ensemble import ExtraTreesClassifier
import numpy as np

from scipy import signal


import datetime

import sys



#sensor = Measurement(trig_pin=19, echo_pin=26)

class Ultrasound_sensors(threading.Thread):
    
    def __init__(self, trig_pin1, echo_pin1, trig_pin2, echo_pin2, out_queue, sample_size, sample_wait, predict_size, train_num):
        
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
        
        self._max_distance1 = 0 #the maximum distance with sensors measuring without passing object
        self._max_distance2 = 0
        
        self._added_numbers_cnt = 1 #added number in front of array for respective sensor
        
        print "Measuring max distance... will take approx 30 seconds."
        self._train_num = train_num
        self._measure_max_distance(train_num)
        
    def run(self):

        #dist1 = []
        #dist2 = []
        
        i = 0
        pred_value = 0
        
        dist12 = self.get_sensor_values(num_values=102, divisor=self._predict_size) 
        
        while(dist12[0].size > 0):

            cni = self._cut_n_inject(dist12, 1, 2, self._predict_size)
            dist1 = cni[0]
            dist2 = cni[1]
            
            if dist2.size > 0:
                #dist2.insert(0, 2)
                pred_value = self._model.predict(dist2)[0] #need to take care of both dist1 and dist2
            
                if pred_value >= self._PASSED_1_TO_2:
                    cdt = datetime.datetime.now()
                    self._queue.put([pred_value]) #[cdt.year, cdt.month, cdt.day, cdt.weekday(), cdt.hour, cdt.minute//10, pred_value])
                
                #dist1 = []
                #dist2 = []
                print "predicted direction: ", pred_value
                    
            i += 1
            
        return
    
    
    
    def _rebuild_sensor_values(self, dist, bf_i_min, divisor):
        
        rebuilt_dist = np.array([])
        
        
        len_dist = len(dist)
        rightmost_index = len_dist-divisor
        
        print "len_dist: ", len_dist
        print "rightmost_index: ", rightmost_index
        
        print "bf_i_min: ", bf_i_min
        
        print "bf_i_min[0]", bf_i_min[0]
        
        for i in bf_i_min[0]:
            print "i: ", i
            if i >= 0 and i <= rightmost_index:
                rebuilt_dist = np.append(rebuilt_dist, dist[i:i+divisor], axis=0)
                continue
            if i < 0:
                rebuilt_dist = np.append(rebuilt_dist, dist[0:divisor], axis=0)
                continue
            if i > rightmost_index:
                rebuilt_dist = np.append(rebuilt_dist, dist[(len_dist-divisor):len_dist], axis=0)
                
                
        while(len(rebuilt_dist) < len_dist):
            rebuilt_dist = np.append(rebuilt_dist, [self._max_distance1], axis=0)
            print "length of rebuilt_dist: ", len(rebuilt_dist)
            
        return rebuilt_dist
    
    
                
    def _frame_sensor_values(self, num_values, divisor, dist1, dist2):
        
        rebuilt_dist1 = np.array([])
        rebuilt_dist2 = np.array([])
        
        min1 = signal.argrelmin(dist1, order=2)
        min2 = signal.argrelmin(dist2, order=2)

        bf_i_min1 = map(lambda x : x - divisor//2, min1) #before indices
        bf_i_min2 = map(lambda x : x - divisor//2, min2) #before indices
        
        rebuilt_dist1 = self._rebuild_sensor_values(dist1, bf_i_min1, divisor)
        rebuilt_dist2 = self._rebuild_sensor_values(dist2, bf_i_min2, divisor)
        
        print "rebuilt_dist1: ", rebuilt_dist1
        print "rebuilt_dist2: ", rebuilt_dist2
        
        return [rebuilt_dist1.flatten(), rebuilt_dist2.flatten()]
            
        
    def get_sensor_values(self, num_values, divisor):
        
        dist1 = np.array([])
        dist2 = np.array([])
        
        i = 0
        
        print "Start triggering sensors in a pattern chosen by you..."
        
        while(i < num_values):
            dist1 = np.append(dist1, [self._sensor1.raw_distance(self._sample_size, self._sample_wait)//1], axis=0)
            dist2 = np.append(dist2, [self._sensor2.raw_distance(self._sample_size, self._sample_wait)//1], axis=0)
            i += 1
    
        sens_values = self._frame_sensor_values(num_values, divisor, dist1, dist2)
        print "sens_values: ", sens_values
        
        return sens_values
    
    
    
    def _measure_max_distance(self, train_num):
        
        
        for i in range(0, train_num):
            self._max_distance1 += self._sensor1.raw_distance(self._sample_size, self._sample_wait)//1
            self._max_distance2 += self._sensor2.raw_distance(self._sample_size, self._sample_wait)//1
            
        
        self._max_distance1 = (self._max_distance1 / train_num)//1
        self._max_distance2 = (self._max_distance2 / train_num)//1 
            
        return
    
    
    
    def _insert_array_in_array(self, X_train, dist, divisor):
    
        print "inside _insert_array_in_array..."
        print "X_train: ", X_train
        print "dist: ", dist
        
        if X_train.size == 0:
            X_train = np.concatenate((X_train, dist), axis=0)
                                     
        elif X_train.size - self._added_numbers_cnt == self._predict_size:
            X_train = np.concatenate(([X_train], [dist]), axis=0)
            
        else:
            X_train = np.concatenate((X_train, [dist]), axis=0)
                
        return X_train
    
    
    def _cut_n_inject(self, dist12, value1, value2, divisor):
        
        dist1p = dist12[0][0:divisor]
        dist2p = dist12[1][0:divisor]

        dist1p = np.insert(dist1p, 0, value1, axis=0)
        dist2p = np.insert(dist2p, 0, value2, axis=0)
        
        dist12[0] = np.delete(dist12[0], np.s_[0:divisor], axis=0)
        dist12[1] = np.delete(dist12[1], np.s_[0:divisor], axis=0)
        
        return [dist1p, dist2p]    
    
    
    def train(self, train_num, divisor):
        
        dist12 = self.get_sensor_values(train_num, divisor)

        X_train1 = np.array([])
        X_train2 = np.array([])
        y1 = np.array([])
        y2 = np.array([])
        
        while(dist12[0].size > 0):
            
            print "dist12", dist12
            
            cni = self._cut_n_inject(dist12, 1, 2, divisor)
            dist1p = cni[0]
            dist2p = cni[1]
            
            
            print "Which direction is the person moving in?\n (0 = no sensor triggered)\n (1 = from sensor1 to sensor2),\n (2 = from sensor2 to sensor1)"
            print "Values depicting sensor1 and sensor2 in a row: "
            print dist1p
            print dist2p
            
            y_val = sys.stdin.read(2)[0]
            y1 = np.append(y1, [y_val], axis=0)
            y_val = sys.stdin.read(2)[0]
            y2 = np.append(y2, [y_val], axis=0)
            
            X_train1 = self._insert_array_in_array(X_train1, dist1p, divisor)
            X_train2 = self._insert_array_in_array(X_train2, dist2p, divisor)
            
            print "X_train1: ", X_train1
            print "X_train1 is instance of ndarray: ", isinstance(X_train1, np.ndarray)
            print "X_train2: ", X_train2
        
        self._model.fit(X_train1, y1)
        self._model.fit(X_train2, y2)
                    
        return
