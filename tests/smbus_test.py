import smbus

bus = smbus.SMBus()  # 0 = /dev/i2c-0 , 1 = /dev/i2c-1
bus.open(1)

#SMBus functions

BMP280_I2CADDR = 0x77

BMP280_CONTROL = 0xF4

BMP280_TEMPDATA = 0xFA


cmd = 0xF3 #set to normal reading etc for register
bus.write_byte_data(BMP280_I2CADDR, BMP280_CONTROL, cmd)

#print bus.read_i2c_block_data(BMP280_I2CADDR, 0xF7) #reads outside memory - not good...
#bus.block_process_call(addr, cmd, []) #Seems to hang Pi...

print bus.read_word_data(BMP280_I2CADDR, 0xF7) #reads 16 bit

#bus.write_quick(0x20)

#bus.read_byte(0x20)

#bus.write_byte(0x20, 0x30)

#bus.read_byte_data(0x20, 0x40)

#bus.write_byte_data(0x20, 0x30, 0x60)

#bus.read_word_data(0x20, 0x40)

#bus.write_word_data(0x20, 0x30, 0x40)

#bus.process_call(0x20, 0x30, 0x40)

#bus.read_block_data(0x20, 0x30)

vals = [0x20, 0x30, 0x40, 0x50]
#bus.write_block_data(0x20, 0x30, vals)

#bus.block_process_call(0x20, 0x30, vals)


#I2C access functions

#bus.read_i2c_block_data(0x20, 0x30)

#bus.write_i2c_block_data(0x20, 0x30, vals)

bus.close()
