# Author: Bastien Wirtz <bastien.wirtz@gmail.com>
#
# Based on the Adafruit BMP280 Driver C++ driver and the BMP085 python lib.
#  - https://github.com/adafruit/Adafruit_BMP280_Library
#  - https://github.com/adafruit/Adafruit_Python_BMP
#
# Datasheet: https://www.adafruit.com/datasheets/BST-BMP280-DS001-11.pdf

import time

# BMP280 default address.
BMP280_I2CADDR = 0x77
BMP280_CHIPID = 0xD0

# BMP280 Registers
BMP280_DIG_T1 = 0x88  # R   Unsigned Calibration data (16 bits)
BMP280_DIG_T2 = 0x8A  # R   Signed Calibration data (16 bits)
BMP280_DIG_T3 = 0x8C  # R   Signed Calibration data (16 bits)
BMP280_DIG_P1 = 0x8E  # R   Unsigned Calibration data (16 bits)
BMP280_DIG_P2 = 0x90  # R   Signed Calibration data (16 bits)
BMP280_DIG_P3 = 0x92  # R   Signed Calibration data (16 bits)
BMP280_DIG_P4 = 0x94  # R   Signed Calibration data (16 bits)
BMP280_DIG_P5 = 0x96  # R   Signed Calibration data (16 bits)
BMP280_DIG_P6 = 0x98  # R   Signed Calibration data (16 bits)
BMP280_DIG_P7 = 0x9A  # R   Signed Calibration data (16 bits)
BMP280_DIG_P8 = 0x9C  # R   Signed Calibration data (16 bits)
BMP280_DIG_P9 = 0x9E  # R   Signed Calibration data (16 bits)

BMP280_CONTROL = 0xF4
BMP280_RESET = 0xE0
BMP280_CONFIG = 0xF5
BMP280_PRESSUREDATA = 0xF7
BMP280_TEMPDATA = 0xFA


class BMP280(object):
    def __init__(self, framework=None, address=None, i2c=None, **kwargs):

	self._framework = framework
	
	if(self._framework != None):
	  self._framework.write_bus('i2c', BMP280_I2CADDR, BMP280_CONTROL, [0x3F])
	  self._load_calibration()


    def _read_calib_registerU(self, calib_register):

	reg_list = self._framework.read_bus('i2c', BMP280_I2CADDR, calib_register, 2)

	val = (reg_list[1] << 8) |  reg_list[0]
        return val


    def _read_calib_registerS(self, calib_register):
        result = self._read_calib_registerU(calib_register)

        if result > 32767:
          result -= 65536

	#print "calib_reg: ", calib_register, " has value: ", result
        return result

    def _load_calibration(self):
        reg_val=self.cal_t1 = int(self._read_calib_registerU(BMP280_DIG_T1))  # UINT16
	print "calib_reg: ", " has value: ", reg_val
        reg_val=self.cal_t2 = int(self._read_calib_registerS(BMP280_DIG_T2))  # INT16
        print "calib_reg: ", " has value: ", reg_val
	reg_val=self.cal_t3 = int(self._read_calib_registerS(BMP280_DIG_T3))  # INT16
        print "calib_reg: ", " has value: ", reg_val
	reg_val=self.cal_p1 = int(self._read_calib_registerU(BMP280_DIG_P1))  # UINT16
        print "calib_reg: ", " has value: ", reg_val
	reg_val=self.cal_p2 = int(self._read_calib_registerS(BMP280_DIG_P2))  # INT16
	print "calib_reg: ", "value: ", reg_val
	reg_val=self.cal_p3 = int(self._read_calib_registerS(BMP280_DIG_P3))  # INT16
	print "calib_reg: ", "value: ", reg_val
	reg_val=self.cal_p4 = int(self._read_calib_registerS(BMP280_DIG_P4))  # INT16
	print "calib_reg: ", "value: ", reg_val
	reg_val=self.cal_p5 = int(self._read_calib_registerS(BMP280_DIG_P5))  # INT16
        print "calib_reg: ", "value: ", reg_val
	reg_val=self.cal_p6 = int(self._read_calib_registerS(BMP280_DIG_P6))  # INT16
        print "calib_reg: ", "value: ", reg_val
	reg_val=self.cal_p7 = int(self._read_calib_registerS(BMP280_DIG_P7))  # INT16
        print "calib_reg: ", "value: ", reg_val
	reg_val=self.cal_p8 = int(self._read_calib_registerS(BMP280_DIG_P8))  # INT16
        print "calib_reg: ", "value: ", reg_val
	reg_val=self.cal_p9 = int(self._read_calib_registerS(BMP280_DIG_P9))  # INT16
       	print "calib_reg: ", "value: ", reg_val

    def _load_datasheet_calibration(self):
        # Set calibration from values in the datasheet example.  Useful for debugging the
        # temp and pressure calculation accuracy.
        self.cal_t1 = 27504
        self.cal_t2 = 26435
        self.cal_t3 = -1000
        self.cal_p1 = 36477
        self.cal_p2 = -10685
        self.cal_p3 = 3024
        self.cal_p4 = 2855
        self.cal_p5 = 140
        self.cal_p6 = -7
        self.cal_p7 = 15500
	self.cal_p8 = -14500
        self.cal_p9 = 6000

    def read_raw(self, register):
        """Reads the raw (uncompensated) temperature or pressure from the sensor."""
        raw = self._framework.read_bus('i2c', BMP280_I2CADDR, register, 3)

        return ((raw[0]<<16) | (raw[1]<<8) | (raw[2])) >> 4

    def _compensate_temp(self, raw_temp):
        """ Compensate temperature """
        t1 = (((raw_temp >> 3) - (self.cal_t1 << 1)) *
              (self.cal_t2)) >> 11

        t2 = (((((raw_temp >> 4) - (self.cal_t1)) *
                ((raw_temp >> 4) - (self.cal_t1))) >> 12) *
              (self.cal_t3)) >> 14

        return t1 + t2

    def read_temperature(self):
        """Gets the compensated temperature in degrees celsius."""
        raw_temp = self.read_raw(BMP280_TEMPDATA)
        compensated_temp = self._compensate_temp(raw_temp)
        temp = float(((compensated_temp * 5 + 128) >> 8)) / 100

        return temp

    def read_pressure(self):
        """Gets the compensated pressure in Pascals."""
        raw_temp = self.read_raw(BMP280_TEMPDATA)
        compensated_temp = self._compensate_temp(raw_temp)
        raw_pressure = self.read_raw(BMP280_PRESSUREDATA)

        p1 = compensated_temp - 128000
        p2 = p1 * p1 * self.cal_p6
        p2 += (p1 * self.cal_p5) << 17
        p2 += self.cal_p4 << 35
        p1 = ((p1 * p1 * self.cal_p3) >> 8) + ((p1 * self.cal_p2) << 12)
        p1 = ((1 << 47) + p1) * (self.cal_p1) >> 33

        if 0 == p1:
            return 0

        p = 1048576 - raw_pressure
        p = (((p << 31) - p2) * 3125) / p1
        p1 = (self.cal_p9 * (p >> 13) * (p >> 13)) >> 25
        p2 = (self.cal_p8 * p) >> 19
        p = ((p + p1 + p2) >> 8) + ((self.cal_p7) << 4)

        return float(p / 256)

    def read_altitude(self, sealevel_pa=101325.0):
        """Calculates the altitude in meters."""
        # Calculation taken straight from section 3.6 of the datasheet.
        pressure = float(self.read_pressure())
        altitude = 44330.0 * (1.0 - pow(pressure / sealevel_pa, (1.0 / 5.255)))
        return altitude

    def read_sealevel_pressure(self, altitude_m=0.0):
        """Calculates the pressure at sealevel when given a known altitude in
        meters. Returns a value in Pascals."""
        pressure = float(self.read_pressure())
        p0 = pressure / pow(1.0 - altitude_m / 44330.0, 5.255)
        return p0

    def tie_framework(self, framework):
	
	self.__init__(framework = framework)

    def get_registers(self):
	dict = {}

	dict['BMP280_I2CADDR'] = 0x77
	dict['BMP280_CHIPID'] = 0xD0
	dict['BMP280_DIG_T1'] = 0x88  # R   Unsigned Calibration data (16 bits)
	dict['BMP280_DIG_T2'] = 0x8A  # R   Signed Calibration data (16 bits)
	dict['BMP280_DIG_T3'] = 0x8C  # R   Signed Calibration data (16 bits)
	
	return dict