import cPickle
import framework

import BMP280_I2C_smbus as bmp280

BMP280_I2CADDR = 0x77
BMP280_DIG_T1 = 0x88  # R   Unsigned Calibration data (16 bits)


sensor = bmp280.BMP280(framework=None)

#print 'Temp = {0:0.2f} *C'.format(sensor.read_temperature())

#print 'Alt = {0:0.2f} *C'.format(sensor.read_altitude(sealevel_pa=101800))

pkl_file = open('a.pkl', 'wb')
cPickle.dump(sensor, pkl_file)
pkl_file.close()

frame = framework.Framework(bus_type='i2c', bus_nr=1, bus_instance=None)
print "reg 0x88, 0x89 values = ", frame.read_bus('i2c', BMP280_I2CADDR, BMP280_DIG_T1, 2)


pkl_file2 = open('a.pkl', 'rb')
bsensor = cPickle.load(pkl_file2)
bsensor.tie_framework(frame)
print "bsensor temp: ", bsensor.read_temperature()

print "bsensor press: ", bsensor.read_pressure()

print "bsensor alt: ", bsensor.read_altitude(sealevel_pa=101640)


#b.printda() 
