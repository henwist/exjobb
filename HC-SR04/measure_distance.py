import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering 

#right sensor seen from front of prototype
#TRIG = 6                                  #Associate pin 23 to TRIG
#ECHO = 13                                  #Associate pin 24 to ECHO

#left  sensor seen from front of prototype
TRIG = 19
ECHO = 26

print "Distance measurement in progress"

GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in

GPIO.add_event_detect(ECHO, GPIO.BOTH)

while True:

  GPIO.output(TRIG, False)                 #Set TRIG as LOW
  #print "Waitng For Sensor To Settle"
  time.sleep(0.060)                            #Delay of 60 ms between measurements (minimum)

  GPIO.output(TRIG, True)                  #Set TRIG as HIGH
  time.sleep(0.00001)                      #Delay of 0.00001 seconds (10 us pulse to start measuring)
  GPIO.output(TRIG, False)                 #Set TRIG as LOW

    #while GPIO.input(ECHO)==0:               #Check whether the ECHO is LOW
     #pulse_start = time.time()              #Saves the last known time of LOW pulse

    #while GPIO.input(ECHO)==1:               #Check whether the ECHO is HIGH
     #pulse_end = time.time()                #Saves the last known time of HIGH pulse 


  GPIO.wait_for_edge(ECHO, GPIO.BOTH)		#wait for rising edge
  pulse_start = time.time()

  GPIO.wait_for_edge(ECHO, GPIO.BOTH)		#wait for falling edge
  pulse_end = time.time()


  pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

  distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
  distance = round(distance, 2)            #Round to two decimal points

  if distance > 2 and distance < 400:      #Check whether the distance is within range
    print "Distance:",distance - 0.5,"cm"  #Print distance with 0.5 cm calibration
  else:
    print "Out Of Range"                   #display out of range
