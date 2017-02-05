import spidev
import time

spi_session = spidev.SpiDev()
spi_session.open(0,0)
spi_session.max_speed_hz = 1200000 # 1.2 MHz

#            reg , settings 
ctrl_meas = [0x74, 0xF3] #When writing to a register with SPI, then reg 0xF4 - 0x80 -> reg 0x74

reply_bytes = spi_session.xfer2(ctrl_meas)

cmd = [0xD0, 0x00] #read sensor address

reply_bytes = spi_session.xfer2(cmd)

print "Id of sensor is: ", reply_bytes


cmd = [0xF7, 0xF8, 0xF9, 0x00]

reply_bytes = spi_session.xfer2(cmd)
print "Pressure is: "  ,reply_bytes


cmd = [0xFA, 0xFB, 0xFC, 0x00]

reply_bytes = spi_session.xfer2(cmd)

print "Temperature is: "  ,reply_bytes

BMP280_DIG_T1 = 0x88
cmd = [BMP280_DIG_T1, 0x00, 0x00]

reply_bytes = spi_session.xfer2(cmd)

print "Calibration data T1 is: "  ,reply_bytes[1:]

spi_session.close()