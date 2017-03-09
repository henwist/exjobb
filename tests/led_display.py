import spidev
import time

spi_session = spidev.SpiDev()
spi_session.open(0,0)
spi_session.max_speed_hz = 400000 # 400 kHz


key = int(raw_input("Enter a character - end with enter:"))
#key = 0

while(key != 114):

	print "key:", key
	digit  = [key]
	print "digit: ", digit

	spi_session.xfer2(digit)
	
	key = int(raw_input("Enter a character - end with enter:"))
	#key += 1
	digit = []
	#time.sleep(0.050)

spi_session.close()
