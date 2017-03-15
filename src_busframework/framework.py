import i2c_bus
import sqlite3

class Framework():
  """Framework for handling code for sensors and buses."""


  def __init__(self, bus_type=None, bus_nr=None, bus_instance=None):
	"""bus_type is one of: {i2c, spi, uart, your_own_constructed_type}.

	bus_nr depends on bus_type but is usually: {0,1,2} for i2c and spi;
	{/dev/serial0, /dev/ttyS0, com3, ...} etc for uart and depending on OS.

	bus_instance is your own construced bus object - if you have made a
	totally new bus on your own. Then the new bus must implement the
	   abstract class AbstractBus."""

	self.buses = {}

	if bus_type == 'i2c':
	  self.buses[bus_type] = i2c_bus.I2CBus(bus_nr)

	if bus_type == 'spi':
	  self.buses[bus_type] = SPIBus(bus_nr)

	if bus_type == 'uart':
	  self.buses[bus_type] = UARTBus(bus_nr)

	if bus_type != None and bus_instance != None:
	  self.buses[bus_type] = bus_instance

	self._conn = sqlite3.connect('framework.db')

	self._c = self._conn.cursor()

	self._c.execute('''CREATE TABLE IF NOT EXISTS
		         Module (module_name text NOT NULL,
		         bus_type text NOT NULL,
   	   	         module_code blob NOT NULL,
		         PRIMARY KEY(module_name, bus_type))''')

	self._conn.commit()







  def add_sensor_module(self, module_file_name=None, module_name=None,
   			bus_type=None):
	"""module_file_name is the name of the file which content will be
	stored in the database.

	module_name is the name of the module. To avoid name clashes - please
	append the distributor's name to the sensor's name: e.g. BMP280_Adafruit.

	bus_type is the type of the bus that the sensor module is aimed at connecting
	to. Could be e.g. {i2c, spi, uart, all, your_own_constructed_type}.
	all if the module is prepared for multiple busses. It could even be a type you
	have made up of your own when contructing a totally new bus_type
	(and implemented the abstract class AbstractBus."""

	if module_file_name != None and module_name != None and bus_type != None:
 	  self._str_mod = open(module_file_name, 'rb').read()

	  self._c.execute('INSERT INTO Module VALUES (?,?,?)',
		   (module_name, bus_type, self._str_mod))

	  self._conn.commit()








  def remove_sensor_module(self, module_name=None,
   			bus_type=None):
	"""module_name is the name of the module to be removed from the sensor database.

	bus_type is the type of the bus that the sensor module is aimed at connecting
	to. Could be e.g. {i2c, spi, uart, all, your_own_constructed_type}."""

	if module_name != None and bus_type != None:


	  self._c.execute('''DELETE FROM Module
			     WHERE module_name=?
			     AND bus_type=?''',
		             (module_name, bus_type))

	  self._conn.commit()




  def get_modules(self):
      self._c.execute('''SELECT name FROM modules''')
      #self._c.commit()
      return self._c.fetchall()




  def remove_all_sensor_modules_from_db(self,
					do_you_really_want_to_delete_all=None):
	"""do_you_really_want_to_delete_all set to Y will remove all modules
	stored in the database. This is destructive and you will have to enter all
	modules manually again by add_sensor_module function - if preferred."""


	if do_you_really_want_to_delete_all == 'Y':
 	  self._c.execute('DELETE FROM Module')

	  self._conn.commit()



  def update_sensor_module(self, column, name, data):
      self._c.execute('''UPDATE modules set %s = %s WHERE 'name' = %s''', column, data, name)



  def fetch_ns_sensor_module(self, module_name=None,
   			bus_type=None):
	"""module_name is the name of the module to be fetched and ns collected
	from the sensor database.

	bus_type is the type of the bus that the sensor module is aimed at connecting
	to. Could be e.g. {i2c, spi, uart, all, your_own_constructed_type}."""

	if module_name != None and bus_type != None:


	  self._c.execute('''SELECT module_code FROM Module
			   WHERE module_name=? AND bus_type=?''',
			   (module_name, bus_type))


	  self._conn.commit()
	  self._module = self._c.fetchone()

	  print self._module[0]

  	  ns = {}

	  exec(self._module[0]) in ns

	  return ns







  def read_bus(self, bus_type, address, register, byte_count, *args):
	return self.buses[bus_type].read(address, register, byte_count, *args)

  def write_bus(self, bus_type, address, register, value_list, *args):
	return self.buses[bus_type].write(address, register, value_list, *args)


#conn.close() to be placed somewhere eventually...
