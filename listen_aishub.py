#!/usr/bin/python3
# listen_aishub.py
# Listen for TCP data stream from AISHub and save data to text

import socket, sys, os, time
import shutil
import logging
from datetime import datetime

"""
Function: Initializes logging file to write errors to
"""
def setup_logger(logger_name, log_file, level=logging.INFO):
	l = logging.getLogger(logger_name)
	formatter = logging.Formatter('%(asctime)s : %(message)s')
	fileHandler = logging.FileHandler(log_file)
	fileHandler.setFormatter(formatter)

	l.setLevel(level)
	l.addHandler(fileHandler)
"""
Function: Main
"""
def main():
	# AISHub IP and port for filtered data
	TCP_IP = 'data.aishub.net'
	TCP_PORT = 4848

	# Declare variables
	working_dir = '/home/ubuntu/aishub_data'
	month_dic={1:'january',2:'february',3:'march',4:'april',5:'may',6:'june',7:'july',8:'august',9:'september',10:'october',11:'november',12:'december'}
	localtime=time.localtime(time.time())
	mon=localtime[1]

	# create socket for TCP stream
	try:
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect((TCP_IP,TCP_PORT))
	except:
		log.error('Initial Connection: Could not connect to %s and port %s'%(TCP_IP,TCP_PORT))
		quit()

	# Create overall log file
	setup_logger('prog_log','/home/ubuntu/aishub_data/prog_log.log')
	log = logging.getLogger('prog_log')
	log.info('Connected to %s on port %s'%(TCP_IP,TCP_PORT))

	##DEBUG
	#out = open(os.path.join(working_dir,'test_bg.txt'),'w')

	while True:

		#get current time [yr,m,d,hr,min,sec,...]
		currtime = time.localtime(time.time())
		curmonth = currtime[1]

		#if moving to the next month, compress previous month
		if curmonth > mon:
			prev = curmonth - 1
			pr_yr = currtime[0]
			if prev < 0:
				prev = 12
				pr_yr = currtime[0] - 1
			prev_mon = month_dic[prev]+'_'+str(pr_yr)
			archive = os.path.join(working_dir,'archive')
			mon = curmonth
			try:
				shutil.make_archive(os.path.join(archive,prev_mon),'zip',os.path.join(working_dir,prev_mon))
			except:
				log.error('Error archiving directory: ',os.path.join(archive,prev_mon))
			else:
				#remove old directory
				try:
					shutil.rmtree(os.path.join(working_dir,prev_mon))
				except:
					log.error('Error removing directory: ',os.path.join(working_dir,prev_mon))

		#see if directory made for that month
		m_dir = month_dic[currtime[1]]+'_'+str(currtime[0])
		mon_dir = os.path.join(working_dir,m_dir)
		writefile = False

		if os.path.exists(mon_dir):
			writefile = True
		else:
			try:
				os.makedirs(mon_dir)
				writefile = True
			except:
				log.info('Error creating output directory: ',mon_dir)

			"""
			else:
				try:
					setup_logger(m_dir+'_log',mon_dir+'/'+m_dir+'_log.log')
					lg = logging.getLogger(m_dir+'_log')
				except:
					log.error('Error creating monthly log file: ',mon_dir+'/'+m_dir+'_log.log')
			"""

		if writefile:

			mn,dy = currtime[1],currtime[2]
			if mn<10:
				mstr = '0'+str(mn)
			else:
				mstr = str(mn)
			if dy<10:
				dstr = '0'+str(dy)
			else:
				dstr = str(dy)

			filename = mstr+dstr+str(currtime[0])+'_aishub_nmea.txt'
			#'a+' appends to the end of the file automatically --> don't have to check if it exists
			output = open(os.path.join(mon_dir,filename),'a+')

			#get time with millisecond as close to actual data aquisition as possible
			ais_time = datetime.utcnow().strftime('%Y%m%dT%H%M%S.%f')[:-3]+'Z '

			#get data from AISHub
			try:
				data = s.recv(1024)
			except:
				try:
					s.close()
				except:
					log.error('Could not close socket connection.')
				else:
					s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
					s.connect((TCP_IP,TCP_PORT))
					log.info('Reconnecting to %s and port %s'%(TCP_IP,TCP_PORT))
			else:
				ais_data = data.decode('ascii',errors='replace')

				if not data:
					log.info('Data Invalid')

				#write to output file
				data_out = ais_data.split('\n')

				for dat in data_out:
					if dat is not '':
						if dat[0] == '!':
							output.write(ais_time+dat)
						else:
							output.write(dat)
			##DEBUG
			#out.write('testing...')
	s.close()

if '__main__' == __name__:
	main()
