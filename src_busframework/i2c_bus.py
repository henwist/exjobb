import smbus
import abstract_bus

class I2CBus(abstract_bus.AbstractBus):

  def __init__(self, bus_nr):
	self._bus = smbus.SMBus(bus_nr)

  def read(self, address, register, byte_count):
	return self._bus.read_i2c_block_data(address, register, byte_count)

  def write(self, address, register, list_values):
	self._bus.write_i2c_block_data(address, register, list_values)


