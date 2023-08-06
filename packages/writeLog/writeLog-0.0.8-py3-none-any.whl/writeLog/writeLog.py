#!/bin/python3
import os
from time import ctime



def writeLog(logfile, version, process, error, msg):
	if process not in os.listdir('/var/log/'):
		os.mkdir(process)
	os.chdir('/var/log/'+process)
	f = open(logfile, 'a+')
	f.write(('*'*25)+'\n')
	f.write(str(process)+'\n')
	f.write(str(ctime())+'\n')
	f.write('\n')
	f.write(str(error)+'\n')
	f.write(str(msg)+'\n')
	f.close()


