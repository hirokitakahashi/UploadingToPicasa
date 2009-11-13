#!/usr/bin/env python

import matplotlib
#matplotlib.use('Agg') # For png output
from pylab import *
import datetime
import re

class NofileError(Exception):
	def __init__(self, filename):
		self.file = filename
	def __str__(self):
		return 'file ' + self.file + ' not found'

class FormatError(Exception):
	def __str__(self):
		return 'format error in file'

def ReadLogFile(filename):
	try:
		f = open(filename, 'r')
	except IOError:
		err = NofileError(filename)
		raise err
		return (None, None, None)
	
	all=f.readlines()	
	# 1st culumn = date
	# 2nd culumn = T1
	# 3rd culumn = T2
	datelist=[]
	T1list=[]
	T2list=[]
	
	for line in all:
		# ignore header line
		if re.compile(r'^\#.*').search(line):
			continue
		else:
			date, time, T1, T2= line.split()
		T1list.append(T1)
		T2list.append(T2)
		try:
			d, m, y = [int(x) for x in date.split('/')]
			h, mi = [int(x) for x in time.split(':')]
		except:
			err = FormatError()
			raise err
			return
		datelist.append(date2num(datetime.datetime(y, m, d, h, mi, 0)))
	f.close()
	return (datelist, T1list, T2list)

def PlotLog(datelist, T1list, T2list, legendStrings=('T1', 'T2'), saveFile={'enable':False, file:None}):
	fig = figure(1)
	ax1 = gca()
	line1 = ax1.plot_date(datelist, T1list, 'b-')
	hold(True)
	line2 = ax1.plot_date(datelist, T2list, 'r-')
	hold(False)
	title('Temperature', fontsize=10)
	
	# Ticks format depending on the time elapsed
	hour_elapsed = 24*(datelist[-1]-datelist[0])
	if hour_elapsed > 24:
		TimeFmt = matplotlib.dates.DateFormatter('%d/%m %H:%M')
		TimeLoc = matplotlib.dates.HourLocator(interval=6)
		TimeLoc2 = matplotlib.dates.HourLocator(interval=1)
	elif hour_elapsed > 12:
		TimeFmt = matplotlib.dates.DateFormatter('%H:%M')
		TimeLoc = matplotlib.dates.HourLocator(interval=3)
		TimeLoc2 = matplotlib.dates.HourLocator(interval=1)
	elif hour_elapsed > 6:
		TimeFmt = matplotlib.dates.DateFormatter('%H:%M')
		TimeLoc = matplotlib.dates.HourLocator(interval=1)
		TimeLoc2 = matplotlib.dates.MinuteLocator(interval=15)
	else:
		TimeFmt = matplotlib.dates.DateFormatter('%H:%M')
		TimeLoc = matplotlib.dates.HourLocator(interval=1)
		TimeLoc2 = matplotlib.dates.MinuteLocator(interval=10)
	
	ax1.xaxis.set_major_formatter(TimeFmt)
	ax1.xaxis.set_major_locator(TimeLoc)
	ax1.xaxis.set_minor_locator(TimeLoc2)
	
	legend((line1, line2), legendStrings, loc = 'upper left')
	if saveFile['enable']:
		matplotlib.backends.backend = 'Agg'
		savefig(saveFile['file'], format='png')
	else:
		matplotlib.backends.backend = 'TkAgg'
		show()

if __name__ == "__main__":
	logfile="temp2.dat"
	figfile="temp2.png"
	date, T1, T2 = ReadLogFile(logfile)
	PlotLog(date, T1, T2, ('chamber', 'flange'), {'enable':True, 'file':'temp2.png'})