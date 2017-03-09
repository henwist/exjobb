import spidev
spidev = spidev.SpiDev()
spidev.open(0,0)
import leddisplay
dis = leddisplay.Leddisplay(spidev, 1)
