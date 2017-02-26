import framework as fr

fra = fr.Framework('i2c', 1)

#clean the db...
fra.remove_all_sensor_modules_from_db('Y')

#Add a module from file to the db.
fra.add_sensor_module('BMP280_I2C_smbus.py', 'BMP280_Adafruit', 'i2c')

#returns a namespace to be used here:
ns = fra.fetch_ns_sensor_module('BMP280_Adafruit', 'i2c')


#print ns

#Yep correct - will instantiate a sensor with contructor.
sensor = ns['BMP280']()

#The sensor will be used with specified framework.
sensor.tie_framework(fra)

#This should be standard for all sensor modules to be able to print
#all the used registers - good when interacting with sensors with interpreter.
print sensor.get_registers()

print "ns['BMP280_DIG_T1']: ", ns['BMP280_DIG_T1']

#Read the T1 register from the i2c bus.

print "T1 register: ", fra.read_bus('i2c', ns['BMP280_I2CADDR'], 
				     ns['BMP280_DIG_T1'], 2)

print "Temperature: {0:0.2f}".format(sensor.read_temperature())

print "Pressure: {0:0.2f}".format(sensor.read_pressure())

#fra.remove_sensor_module('BMP280_Adafruit', 'i2c')

