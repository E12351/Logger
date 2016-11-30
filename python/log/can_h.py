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

class can(object):

	def read_can(self):

		self.path_can

		d_obj_c = data_H("",data_H.CVS_name_can)

		# data_H.CVS_name_bat	= data_H.CVS_name_can

		data_raw2		= ''
		ser_can 		= serial.Serial(self.path_can,115200, timeout=2, xonxoff=True, rtscts=True, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
		ser_can.flushInput()
		ser_can.flushOutput()

		while True:
			data_raw2= ser_can.readline()

			# for x in xrange(1,len(data_raw2)):
			# 	print data_raw2[0:2]
			print str(data_raw2)
			self.send_C = ''
			if (data_raw2[1:6] == 'ID: BB') :
				# print str(data_raw2[23:25])
				trq = data_raw2[26:37].split(' ')

				trq_hex = str(trq[1]+trq[2]+trq[3])

				xrF = int(trq_hex, 16)
				xrI = int(trq[0],16)
				# print str(trq[0])

				self. send_C ='BB,'+str(xrI)+','+str(xrF)
				# print send_C
			if (data_raw2[1:6] == 'ID: BC') :
				# print str(data_raw2[23:25])
				trq = data_raw2[26:37].split(' ')

				trq_hex = str(trq[1]+trq[2]+trq[3])

				xrF = int(trq_hex, 16)
				xrI = int(trq[0],16)
				# print str(trq[0])

				self.send_C ='BC,'+str(xrI)+','+str(xrF)

			if (data_raw2[0:6] == 'ID: C1') :
				# pass
				# DCm_trip = int(data_raw2[14:15],16)

				# print data_raw2[14:16] + '---' + data_raw2[17:19]

				L_C =int(data_raw2[14:16],16)
				DCm_trip_tmp =bin(L_C) #convert into binary

				DCm_trip_len = len(DCm_trip_tmp)

				DCm_trip = DCm_trip_tmp[2:DCm_trip_len]

				lenth1 = 10-DCm_trip_len

				for x in xrange(1,lenth1+1):
					DCm_trip = '0'+ DCm_trip

				# print 'C1 Trip Events : '+ str(DCm_trip)

				I_C = int(data_raw2[17:19],16)
				DCm_Data_tmp =bin(I_C)
				

				DCm_Data_len = len(DCm_Data_tmp)
				# print DCm_Data_len
				DCm_Data = DCm_Data_tmp[2:DCm_Data_len]

				lenth2 = 10-DCm_Data_len

				for x in xrange(1,lenth2+1):
					DCm_Data = '0'+ DCm_Data

				DCm_Data = '0b'+DCm_Data
				# print str(DCm_Data)
				
				#concat all trip events to one string
				# print DCm_Data
				# print DCm_trip
				DCm_trip = DCm_trip + DCm_Data[6:10]
				# print 'C1 Trip Events : '+ str(DCm_trip)

				if( DCm_Data[2:4] == '10' ):
					# print int(data_raw2[35:37],16)

					BUS_I_t = data_raw2[20:22]
					BUS_I_t = data_raw2[23:25]+BUS_I_t
					
					BUS_I_f = int(BUS_I_t,16)
					# print BUS_I_f

					BUS_v1_t = data_raw2[26:28]
					BUS_v1_t = data_raw2[29:31] + BUS_v1_t
					
					BUS_v1_f = int(BUS_v1_t,16)
					# print BUS_v1_f

					BUS_v2_t = data_raw2[32:34]
					BUS_v2_t = data_raw2[35:37]+ BUS_v2_t
					
					BUS_v2_f = int(BUS_v2_t,16)

					# print 'BUS_I : '+str(BUS_I_t)+' BUS_V1 : '+str(BUS_v1_t)+' BUS_V2 : '+str(BUS_v2_t)

					# print 'BUS_I : '+str(BUS_I_f)+' BUS_V1 : '+str(BUS_v1_f)+' BUS_V2 : '+str(BUS_v2_f)

					self.send_C = 'C1VI,'+str(BUS_I_f)+','+str(BUS_v1_f)+','+str(BUS_v2_f)+','+DCm_trip+','

				if( DCm_Data[2:4] == '01' ):

					IGBT1 = int(data_raw2[20:22],16)
					IGBT2 = int(data_raw2[23:25],16)
					MOTOR_TEMP = int(data_raw2[26:28],16)
					HEATSINK_TEMP = int(data_raw2[29:31],16)
					VS = int(data_raw2[32:34],16)
					IS = int(data_raw2[35:37],16)

					# print 'pass'
					# print 'IGBT : ' +str(IGBT2)

					self.send_C ='C1IGBT1,' + str(IGBT1)+','+str(IGBT2)+','+str(MOTOR_TEMP)+','+str(HEATSINK_TEMP)+','+str(VS)+','+str(IS)+','+DCm_trip+','


				#-----------------
				if( DCm_Data[2:4] == '00' ):

					# print'Data Pack : 00'
					SW_F = int(data_raw2[20:22],16)
					BUS_I = int(data_raw2[23:25],16)
					BUS_V1 = int(data_raw2[26:28],16)
					BUS_V2 = int(data_raw2[29:31],16)
					MOTOR_PW = int(data_raw2[32:34],16)
					IGBT0 = int(data_raw2[35:37],16)
					# print IGBT0
					self.send_C ='C1IGBT0,' +str(IGBT0)+','+str(BUS_I)+','+str(BUS_V1)+','+str(BUS_V2)+','+str(MOTOR_PW)+','+DCm_trip+','
			

			if (data_raw2[0:6] == 'ID: C2') :
				# pass
				# DCm_trip = int(data_raw2[14:15],16)

				# print data_raw2[14:16] + '---' + data_raw2[17:19]

				L_C =int(data_raw2[14:16],16)
				DCm_trip_tmp =bin(L_C) #convert into binary

				DCm_trip_len = len(DCm_trip_tmp)

				DCm_trip = DCm_trip_tmp[2:DCm_trip_len]

				lenth1 = 10-DCm_trip_len

				for x in xrange(1,lenth1+1):
					DCm_trip = '0'+ DCm_trip

				# print 'C1 Trip Events : '+ str(DCm_trip)

				I_C = int(data_raw2[17:19],16)
				DCm_Data_tmp =bin(I_C)
				

				DCm_Data_len = len(DCm_Data_tmp)
				# print DCm_Data_len
				DCm_Data = DCm_Data_tmp[2:DCm_Data_len]

				lenth2 = 10-DCm_Data_len

				for x in xrange(1,lenth2+1):
					DCm_Data = '0'+ DCm_Data

				DCm_Data = '0b'+DCm_Data
				# print str(DCm_Data)
				
				#concat all trip events to one string
				# print DCm_Data
				# print DCm_trip
				DCm_trip = DCm_trip + DCm_Data[6:10]
				# print 'C1 Trip Events : '+ str(DCm_trip)

				if( DCm_Data[2:4] == '10' ):
					# print int(data_raw2[35:37],16)

					BUS_I_t = data_raw2[20:22]
					BUS_I_t = data_raw2[23:25]+BUS_I_t
					
					BUS_I_f = int(BUS_I_t,16)
					# print BUS_I_f

					BUS_v1_t = data_raw2[26:28]
					BUS_v1_t = data_raw2[29:31] + BUS_v1_t
					
					BUS_v1_f = int(BUS_v1_t,16)
					# print BUS_v1_f

					BUS_v2_t = data_raw2[32:34]
					BUS_v2_t = data_raw2[35:37]+ BUS_v2_t
					
					BUS_v2_f = int(BUS_v2_t,16)

					# print 'BUS_I : '+str(BUS_I_t)+' BUS_V1 : '+str(BUS_v1_t)+' BUS_V2 : '+str(BUS_v2_t)

					# print 'BUS_I : '+str(BUS_I_f)+' BUS_V1 : '+str(BUS_v1_f)+' BUS_V2 : '+str(BUS_v2_f)

					self.send_C = 'C2VI,'+str(BUS_I_f)+','+str(BUS_v1_f)+','+str(BUS_v2_f)+','+DCm_trip+','

				if( DCm_Data[2:4] == '01' ):

					IGBT1 = int(data_raw2[20:22],16)
					IGBT2 = int(data_raw2[23:25],16)
					MOTOR_TEMP = int(data_raw2[26:28],16)
					HEATSINK_TEMP = int(data_raw2[29:31],16)
					VS = int(data_raw2[32:34],16)
					IS = int(data_raw2[35:37],16)

					# print 'pass'
					# print 'IGBT : ' +str(IGBT2)

					self.send_C ='C2IGBT1,' + str(IGBT1)+','+str(IGBT2)+','+str(MOTOR_TEMP)+','+str(HEATSINK_TEMP)+','+str(VS)+','+str(IS)+','+DCm_trip+','


				#-----------------
				if( DCm_Data[2:4] == '00' ):

					# print'Data Pack : 00'
					SW_F = int(data_raw2[20:22],16)
					BUS_I = int(data_raw2[23:25],16)
					BUS_V1 = int(data_raw2[26:28],16)
					BUS_V2 = int(data_raw2[29:31],16)
					MOTOR_PW = int(data_raw2[32:34],16)
					IGBT0 = int(data_raw2[35:37],16)
					# print IGBT0
					self.send_C ='C2IGBT0,' +str(IGBT0)+','+str(BUS_I)+','+str(BUS_V1)+','+str(BUS_V2)+','+str(MOTOR_PW)+','+DCm_trip+','
		

			# if (data_raw2[0:6] == 'ID: C1') :
			# 	print '--------------------------------'+str(data_raw2)

			# data_raw2 = 'C,ID: BB  Data: 00 00 00 AA 01 8A 26 59'
			# time.sleep(0.5)
			# print
			time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			csv_write_can = time+' ' + str(data_raw2)

			# print 'CAN data : '+str(data_raw2)

			if str(data_raw2) != '':
				d_obj_c.data = csv_write_can.split(',')
				data_H.csv_writer(d_obj_c)

			data_H.lock.acquire()
			if data_H.q.full():
				data_H.q.get()
				print 'Data droped : CAN'
			self.send_C = 'C,'+ self.send_C
			print str(self.send_C)
			data_H.q.put(self.send_C)
			data_H.lock.release()
