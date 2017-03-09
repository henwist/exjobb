import time
import decimal

class Leddisplay():
	"""Class for writing numbers (integer as well as float) to 
	a led display segmented as 7 segments plus decimal point on
	a SPI bus using spidev class."""
	def __init__(self, spidev, sleep_ms):
		self._spidev = spidev
		self._spidev.max_speed_hz = 400000 #400 kHz
		self._segment_a = 1<<1
		self._segment_b = 1<<2
		self._segment_c = 1<<5
		self._segment_d = 1<<4
		self._segment_e = 1<<3
		self._segment_f = 1<<0
		self._segment_g = 1<<6
		self._segment_dp = 1<<7

		self._numdict = {}

		self._numdict['0'] = self._segment_a | self._segment_b | self._segment_c | self._segment_d | self._segment_e | self._segment_f
		self._numdict['1'] = self._segment_b | self._segment_c
		self._numdict['2'] = self._segment_a | self._segment_b | self._segment_g | self._segment_e | self._segment_d
		self._numdict['3'] = self._segment_a | self._segment_b | self._segment_g | self._segment_c | self._segment_d
		self._numdict['4'] = self._segment_f | self._segment_g | self._segment_b | self._segment_c
		self._numdict['5'] = self._segment_a | self._segment_f | self._segment_g | self._segment_c | self._segment_d
		self._numdict['6'] = self._segment_f | self._segment_e | self._segment_d | self._segment_c | self._segment_g
		self._numdict['7'] = self._segment_a | self._segment_b | self._segment_c
		self._numdict['8'] = self._segment_a | self._segment_b | self._segment_c | self._segment_d | self._segment_e | self._segment_f | self._segment_g
		self._numdict['9'] = self._segment_a | self._segment_b | self._segment_c | self._segment_f | self._segment_g
		self._numdict['.'] = self._segment_dp
		self._numdict['-'] = self._segment_g
		self._numdict['u'] = self._segment_c | self._segment_d | self._segment_e

		self._minimum_number = decimal.Decimal('0.0000001')
		self._minimum_number_neg = decimal.Decimal('-0.0000001')

		self._num_list = []
		self._remainder_list = []
	
		self._sleep_ms = sleep_ms

		decimal.getcontext().prec = 7

	def _remove_zeros(self, d):
		return d.normalize()



	def _print_to_display(self, numberlist):
		
		latest_printed_char = 'u'

		for n in numberlist:
			if n == latest_printed_char: #to be able to distinguish a number from the former printed one.
				self._spidev.xfer2([self._numdict['u']])
				time.sleep(0.5)

			latest_printed_char = n
			self._spidev.xfer2([self._numdict[n]])
			time.sleep(self._sleep_ms)
			print "n:", n

	def _conditionally_prepare_remainder(self, whole_integral):
		
		if len(self._remainder_list) > 1:

			if self._remainder_list[0] == '0':
				self._remainder_list = self._remainder_list[1:] #remove the zero from the beginning

			if self._remainder_list[0] == '-' and self._remainder_list[1] == '0' and whole_integral <= -0:
				del self._remainder_list[0]
				del self._remainder_list[0]

			print "whole_integral:" , whole_integral

	
	def _conditionally_print_number(self, whole_integral, remainder):
		
		if len(self._num_list) > 0:
                        self._print_to_display(self._num_list)

			self._conditionally_prepare_remainder(whole_integral)
                        self._print_to_display(self._remainder_list)

                else:
                        self._print_to_display(self._remainder_list)


	def print_num(self, number):
		"""Writes out a number to a led display. number can be
		a float as well as an integer in base 10. Up to seven
		digits after decimal (dot) will be written to bus. If 
		there are more digits, they will be truncated."""

		D = decimal.Decimal
		
		d = D(str(number))
		whole_integral = d // 1
		
		remainder = 0
	  	remainder = self._remove_zeros(d % 1) if remainder >= 0 else self._remove_zeros(d%(-1))
			
		self._num_list = [str(i) for i in whole_integral.to_eng_string()]

                if remainder >= self._minimum_number or remainder <= self._minimum_number_neg:
                        self._remainder_list = [str(i) for i in remainder.to_eng_string()]

		self._conditionally_print_number(whole_integral, remainder)


		print "remainder_list", self._remainder_list

		self._num_list = []
		self._remainder_list = []

	def __str__(self):
		return "This object is used for communication with a 7-segment display."


