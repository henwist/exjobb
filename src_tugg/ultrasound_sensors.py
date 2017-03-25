import threading
from hcsr04sensor.sensor import Measurement
import Queue

from sklearn.ensemble import ExtraTreesClassifier
import numpy as np

from scipy import signal


import datetime

import sys

from sklearn.externals import joblib


np.set_printoptions(precision=0, suppress=True)



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
        self._RESET_VALUE = -1
        self._MAX_NUM_OF_MAX_DIST = 11
        
        self._predict_size = predict_size
        
        self._min_distance = 2 #minimum distance the sensor can handle (cm)
        self._max_distance1 = 0 #the maximum distance with sensors measuring a rigid object (background)
        self._max_distance2 = 0
        
        self._added_numbers_cnt = 1 #added number in front of array for respective sensor
        
        print "Measuring max distance... will take approx 30 seconds."
        self._train_num = train_num
        self._measure_max_distance(self._MAX_NUM_OF_MAX_DIST)
        
        self._model_file_name = './model/extra_trees_classifier.pkl'
        self._is_model_loaded = False
        
    def run(self):
        """This function is the threads main function."""
        
        if self._is_model_loaded == False:
            print "Loading model from file...takes approx 30 seconds."
            self._model = joblib.load(self._model_file_name)
            self._is_model_loaded = True
        
        i = 0
        pred_value = 0
        
        dist12 = self.get_sensor_values(num_values=102, divisor=self._predict_size) 
        
        while(dist12[0].size > 0):

            cni = self._cut_n_inject(dist12, 1, 2, self._predict_size)
            dist1 = cni[0]
            dist2 = cni[1]
            
            print "run: dist1: ", dist1
            print "run: dist2: ", dist2
            
            if dist2.size > 0:
                #dist2.insert(0, 2)
                pred_value1 = self._model.predict(dist1)[0]
                pred_value2 = self._model.predict(dist2)[0]
                
                if pred_value1 >= self._PASSED_1_TO_2 or pred_value2 >= self._PASSED_1_TO_2:
                    cdt = datetime.datetime.now()
                    self._queue.put([pred_value1]) #[cdt.year, cdt.month, cdt.day, cdt.weekday(), cdt.hour, cdt.minute//10, pred_value])
                    self._queue.put([pred_value2])
                
                #dist1 = []
                #dist2 = []
                print "[pred_value1, pred_value2]: ", [pred_value1, pred_value2]
                print ""
                    
            i += 1
            
        return
    
    
    
    def _rebuild_sensor_values(self, dist, bf_i_min, divisor):
        """This function rebuilds the array of sensor values
        to a format where all values are inside the array
        and missing values are replaced with a mean value."""
        
        rebuilt_dist = np.array([], dtype=np.uint16)
        
        
        len_dist = len(dist)
        rightmost_index = len_dist-divisor
        
        #print "len_dist: ", len_dist
        #print "rightmost_index: ", rightmost_index
        
        #print "bf_i_min: ", bf_i_min
        
        #print "bf_i_min[0]", bf_i_min[0]
        
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
                
                
        while(len(rebuilt_dist) < len_dist): #append a standard value to fill the array to it's original size
            rebuilt_dist = np.append(rebuilt_dist, [self._max_distance1], axis=0)
            #print "length of rebuilt_dist: ", len(rebuilt_dist)
            
        return rebuilt_dist.astype(dtype=np.uint16)
    
    
                
    def _frame_sensor_values(self, num_values, divisor, dist1, dist2):
        """This function frames a row of sensor values depending on
        the divisor and where the min values are situated
        in the array"""
        
        rebuilt_dist1 = np.array([], dtype=np.uint16)
        rebuilt_dist2 = np.array([], dtype=np.uint16)
        
        min1 = signal.argrelmin(dist1, order=2)
        min2 = signal.argrelmin(dist2, order=2)

        bf_i_min1 = map(lambda x : x - divisor//2, min1) #before indices
        bf_i_min2 = map(lambda x : x - divisor//2, min2) #before indices
        
        rebuilt_dist1 = self._rebuild_sensor_values(dist1, bf_i_min1, divisor)
        rebuilt_dist2 = self._rebuild_sensor_values(dist2, bf_i_min2, divisor)
        
        #print "rebuilt_dist1: ", rebuilt_dist1
        #print "rebuilt_dist2: ", rebuilt_dist2
        
        return [rebuilt_dist1.flatten().astype(dtype=np.uint16), rebuilt_dist2.flatten().astype(dtype=np.uint16)]
            
        
    def get_sensor_values(self, num_values, divisor):
        """This function reads num_values values from the
        two sensors. A divisor is needed to be able to
        assign a row of values to a specific sensing 
        moment"""
        
        dist1 = np.array([], dtype=np.uint16)
        dist2 = np.array([], dtype=np.uint16)
        
        i = 0
        
        print "Start triggering sensors in a pattern chosen by you..."
        
        while(i < num_values):
            dist1 = np.append(dist1, [self._sensor1.raw_distance(self._sample_size, self._sample_wait)//1], axis=0)
            dist2 = np.append(dist2, [self._sensor2.raw_distance(self._sample_size, self._sample_wait)//1], axis=0)
            i += 1
    
        dist1 = np.clip(dist1, self._min_distance, self._max_distance1) #exchange values outside limits to limit values
        dist2 = np.clip(dist2, self._min_distance, self._max_distance2) #exchange values outside limits to limit values
        
        sens_values = self._frame_sensor_values(num_values, divisor, dist1, dist2)
        #print "sens_values: ", sens_values
        
        return sens_values
    
    
    
    def _measure_max_distance(self, train_num):
        """This funcion measures the max distance the 
        sensor may read and stores the mean from the 
        values read."""
        
        for i in range(0, train_num):
            self._max_distance1 += self._sensor1.raw_distance(self._sample_size, self._sample_wait)//1
            self._max_distance2 += self._sensor2.raw_distance(self._sample_size, self._sample_wait)//1
            
        
        self._max_distance1 = (self._max_distance1 / train_num)//1
        self._max_distance2 = (self._max_distance2 / train_num)//1 
            
        return
    
    
    
    def _insert_array_in_array(self, X_train, dist, divisor):
        """This function inserts an array into a bigger array.
        It is needed as there exists different ways to insert
        an array depending on how the main array looks at 
        the moment"""
        
        #print "inside _insert_array_in_array..."
        #print "X_train: ", X_train
        #print "dist: ", dist
        
        if X_train.size == 0:
            X_train = np.concatenate((X_train, dist), axis=0)
                                     
        elif X_train.size - self._added_numbers_cnt == self._predict_size:
            X_train = np.concatenate(([X_train], [dist]), axis=0)
            
        else:
            X_train = np.concatenate((X_train, [dist]), axis=0)
                
        return X_train.astype(dtype=np.uint16)
    
    
    def _cut_n_inject(self, dist12, value1, value2, divisor):
        """This function injects a sensor number into an
        array of sensor values. It also shortens the main
        input array when the values have been taken out and
        transferred to smaller arrays."""
        
        dist1p = dist12[0][0:divisor]
        dist2p = dist12[1][0:divisor]

        dist1p = np.insert(dist1p, 0, value1, axis=0)
        dist2p = np.insert(dist2p, 0, value2, axis=0)
        
        dist12[0] = np.delete(dist12[0], np.s_[0:divisor], axis=0)
        dist12[1] = np.delete(dist12[1], np.s_[0:divisor], axis=0)
        
        return [dist1p, dist2p]    
    
    
    
    def _input_triggered_sensors(self, dist1p, dist2p):
        """This function assigns a sensor number to an array
        of values."""

        y1_val = self._RESET_VALUE
        y2_val = self._RESET_VALUE
        
        print "Enter a 1 for a triggered sensor and a 0 for other cases:"
        
        print "Values depicting sensor1 and sensor2 in a row: "
        print dist1p
        print dist2p
        
        while(y1_val != '0' and y1_val != '1'):
            y1_val = sys.stdin.read(2)[0]
            print y1_val
        
        
        while(y2_val != '0' and y2_val != '1'):
            y2_val = sys.stdin.read(2)[0]
            print y2_val
        
        return [y1_val, y2_val]
    
    
    
    
    def train(self, train_num, divisor):
        """This function is used to train the sensors to 
        be able to recognise a person passing the sensors."""
        
        dist12 = self.get_sensor_values(train_num, divisor)

        X_train1 = np.array([], dtype=np.uint16)
        X_train2 = np.array([], dtype=np.uint16)
        y1 = np.array([], dtype=np.uint16)
        y2 = np.array([], dtype=np.uint16)
        
        while(dist12[0].size > 0):
            
            print "dist12", dist12
            
            cni = self._cut_n_inject(dist12, 1, 2, divisor)
            dist1p = cni[0]
            dist2p = cni[1]
            
            y1_val, y2_val = self._input_triggered_sensors(dist1p, dist2p)
            y1 = np.append(y1, [y1_val], axis=0)
            y2 = np.append(y2, [y2_val], axis=0)
            
            X_train1 = self._insert_array_in_array(X_train1, dist1p, divisor)
            X_train2 = self._insert_array_in_array(X_train2, dist2p, divisor)
            
            
        
        if self._is_model_loaded == False:
            print "Loading model from file...takes approx 30 seconds."
            self._model = joblib.load(self._model_file_name)
            self._is_model_loaded = True
            
        print "train: X_train1: ", X_train1
        print "train: X_train2: ", X_train2
        print "y1: ", y1    
        print "y2: ", y2
        
        print "Training model..."
        self._model.fit(X_train1.astype(dtype=np.uint16), y1.astype(dtype=np.uint16))
        self._model.fit(X_train2.astype(dtype=np.uint16), y2.astype(dtype=np.uint16))
        print "Training finished."
        
        print "Dumping model to file...takes approx 30 seconds."
        joblib.dump(self._model, self._model_file_name)
        print "Dumping finished."
                    
        return
