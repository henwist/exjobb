import i2c_bus

class Framework():

  def __init__(self, bus_type=None, bus_nr=None, bus_instance=None):
	self.buses = {}

	if bus_type == 'i2c':
	  self.buses[bus_type] = i2c_bus.I2CBus(bus_nr)

	if bus_type == 'spi':
	  self.buses[bus_type] = SPIBus(bus_nr)

	if bus_type == 'uart':
	  self.buses[bus_type] = UARTBus(bus_nr)
	
	if bus_type != None and bus_instance != None:
	  self.buses[bus_type] = bus_instance
  
  def read_bus(self, bus_type, address, register, byte_count, *args):
	return self.buses[bus_type].read(address, register, byte_count, *args)

  def write_bus(self, bus_type, address, register, value_list, *args):
	return self.buses[bus_type].write(address, register, value_list, *args)
