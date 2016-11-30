import csv
import serial
import serial.tools.list_ports
import thread
import threading
import time
import Queue
import os
import errno
import time
import struct
import shutil
import sys
import re

from Data_H import data_H
from sys import stdout
from time import sleep
from datetime import datetime
from threading import Thread

class bat(object):

	def read_battery(self):

		self.path_can
		d_obj_b = data_H("",data_H.CVS_name_bat_1_vol)
		# data_H.CVS_name_bat	= data_H.CVS_name_bat_1_vol

		ser_batt = serial.Serial(self.path_can, 9600, timeout=2, xonxoff=True, rtscts=True, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
		# ser_batt = serial.Serial(self.path_can, 115200, timeout=2, xonxoff=True, rtscts=True, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
		ser_batt.flushInput()
		ser_batt.flushOutput()

		B1T='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
		B2T='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
		Current='xx'

		while True:
			# start_time = time.time()
			line = ""
			no_of_bat = ''
			# time.sleep(0.001)

			x = ser_batt.readline(1)

			# if x == '#':
			# 	while True:
			# 		x = ser_batt.readline(1)
			# 		if (x == '$'):
			# 			line = ""
			# 		# else:
			# 		# if (x != '#') | (x != '$'):
			# 		line = line + str(x)
			# 		if (x == '\n') | (x == '\t'):
			# 			print str(line)
			# 			lenb = len(line)
			# 			if lenb < 75:
			# 				line = 'T,' + line
			# 			else:
			# 				line = 'B,' + line
			# 			break
			#---------------------------------------
			if x == '#':
				while True:
					x = ser_batt.readline(1)
					# print x
					time1 = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]

					try:
						if (x == '$'):
							line = ""
						line = line + str(x)
						if x == '\t':
							# ----------------------------
							if line[0] =='$':
								no_of_bat_TEMP = str(line[3])
								# print str(no_of_bat_TEMP)
							else:
								no_of_bat_TEMP = str(line[1])
								# print str(no_of_bat_TEMP)

							if no_of_bat_TEMP == '1':
									# line = 'T,'+line
									B1T=''
									B1T = line
									
							if no_of_bat_TEMP == '2':
									# line = 'T,'+line
									B2T=''
									B2T = line
									
							# ----------------------------
							# print str(line)
							line = 'T,' + line
							# data_H.data = ''

							# Battery tem Log----------------------------------
							# d_obj_b.CVS_name_bat	= data_H.CVS_name_bat_temp
							# csv_write_battery = time1 + str(line)
							# d_obj_b.data = csv_write_battery.split(',')
							# # print str(d_obj_b.data)
							# data_H.csv_writer(d_obj_b)
							# --------------------------------------------------
							break
						if x =='\n':
							if line[0] =='$':
								# print str(line[3])
								no_of_bat = str(line[3])
							else:
								# print str(line[1])
								no_of_bat = str(line[1])

							line = ' B,' + line
							break

					except Exception,e:
						print 'ERROR corrupted data : '+str(e)

			#---------------------------------------
				# print no_of_bat
				if no_of_bat == '3':
					# print line[2:7]
					Current = line
				if no_of_bat == '1':
					# data_H.data = ''
					csv_write_battery = time1 +str(Current)+str(B1T) +str(line)
					d_obj_b.CVS_name_bat	= data_H.CVS_name_bat_1_vol
					d_obj_b.data = csv_write_battery.split(',')
					data_H.csv_writer(d_obj_b)

				if no_of_bat == '2':

					# data_H.data = ''
					csv_write_battery = time1 +str(Current)+ str(B2T)+ str(line)
					d_obj_b.CVS_name_bat	= data_H.CVS_name_bat_2_vol
					d_obj_b.data = csv_write_battery.split(',')
					data_H.csv_writer(d_obj_b)

				data_H.lock.acquire()
				if data_H.q.full():
					data_H.q.get()
					print 'Data droped : BATTERY'
				# print line
				data_H.q.put(line)
				data_H.lock.release()
