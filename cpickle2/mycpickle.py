import sys
sys.path.append('../src_busframework/')

import sqlite3
import framework

conn = sqlite3.connect('sensor.db')

c = conn.cursor()

#c.execute('''CREATE TABLE Module (module_name text NOT NULL PRIMARY KEY, module_code blob NOT NULL)''')
#c.execute('''CREATE TABLE Sensor (python blob)''')


#str_mod = open('BMP280_I2C_smbus.py', 'rb').read()

#c.execute('INSERT INTO Module VALUES (?,?)', ('BMP280_Adafruit', str_mod))
#conn.commit()

c.execute('SELECT module_code FROM Module WHERE module_name=\'BMP280_Adafruit\';')

conn.commit()

module = c.fetchone()

print module[0]

exec(module[0])
 
bsensor = BMP280()

frame = framework.Framework(bus_type='i2c', bus_nr=1, bus_instance=None)
bsensor.tie_framework(frame, 'i2c')

print "bsensor temp: {0:0.2f}".format(bsensor.read_temperature())

print "bsensor press: {0:0.2f}".format(bsensor.read_pressure())

print "bsensor alt: {0:0.2f}".format(bsensor.read_altitude(sealevel_pa=100740))

conn.close()