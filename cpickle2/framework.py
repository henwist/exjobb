import abc
import smbus
import time

class AbstractBus:
  __metaclass__ = abc.ABCMeta

  @abc.abstractmethod
  def read(self):
   raise NotImplementedError("Class %s  needs to implement " %(self.__class__.__name__))

  @abc.abstractmethod
  def write(self):
   raise NotImplementedError("Class %s needs to implement " %(self.__class__.__name__))



class I2CBus(AbstractBus):

  def __init__(self, bus_nr):
	self._bus = smbus.SMBus(bus_nr)

  def read(self, address, register, byte_count):
	return self._bus.read_i2c_block_data(address, register, byte_count)

  def write(self, address, register, list_values):
	self._bus.write_i2c_block_data(address, register, list_values)


class Framework():

  def __init__(self, bus_type=None, bus_nr=None, bus_instance=None):
	self.buses = {}

	if bus_type == 'i2c':
	  self.buses[bus_type] = I2CBus(bus_nr)

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
