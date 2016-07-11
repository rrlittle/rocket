# import some useful stuff
import logging
from inspect import getmembers, isclass, isfunction
import argparse
import tkinter
from tkinter.filedialog import askopenfilename, asksaveasfilename
from csv import DictReader, DictWriter
from os.path import join, abspath, isfile
import platform
from os import environ
from collections import OrderedDict
from importlib import import_module
from sys import exit


class null_logging: 
	''' an empty logger that can be used instead pf logging
		hopefully this will help stop double printing using
		the logging module. 
		'''
	def debug():pass
	def info():pass
	def warning():pass
	def error():pass
	def critical():pass
null_log = null_logging() # default logger

def make_logger(logname, 
	frmt='%(name)s:%(levelname)s[%(filename)s.%(funcName)s]>%(message)s', 
	fpath=None, 
	stdout=True, 
	flvl=None,
	lvl=logging.DEBUG): 
	''' makes a simple intuitive logger. every time you call this
		you can define what it will look like and where ii will go etc. 
		if fpath is provided it will log to a file given by fpath. 
		by defualt the file will have the same level as the logger. but you can
		override that with flvl to be any logging level
		CRITICAL	50
		ERROR	40
		WARNING	30
		INFO	20
		DEBUG	10
		NOTSET	0

		when this is created the logfile is truncated. but then appended to. 
		so if your manking a bunch of these you should make them all at the beginning
		so you truncate a few times and then fill it up from a varitey of sources. 
		'''
	l = logging.getLogger(logname)
	l.setLevel(logging.DEBUG) 
	# the base will see everything and handlers will decide
	f = logging.Formatter(frmt)
	if stdout: 
		sh = logging.StreamHandler()
		sh.setFormatter(f)
		sh.setLevel(lvl)
		l.addHandler(sh)
	if fpath:
		fh = logging.FileHandler(fpath, mode='a')
		fh.setFormatter(f)
		if flvl: fh.setLevel(flvl)
		else: fh.setLevel(lvl)
		l.addHandler(fh)

	return l
def truncfile(fpath):
	if isfile(fpath): # if it's an exisiting file, truncate it  
		f = open(fpath, mode='w')
		f.truncate()
		f.close()

# run som setup stuff
systemName = platform.system()
tkinter.Tk().withdraw()

# define some useful functions
def make_args(description, args = {}):
	''' this returns a parser for requiring arguments
		to run the package. 
		description is a string describing the project
		args is a dictionary of arguments and their various 
		attributes as described by the default. 
		the attributes can be anything argsparse.add_argument takes
	'''
	parser = argparse.ArgumentParser(description=description)
	for arg in args:
		parser.add_argument(arg, **args[arg])
	return parser

def load_handlers():
	''' this loads the handlers from 
		.data_handlers if any.

		returns {
			'source':{name:handler class refs},
			'sink':{name:handler class refs}
		}
	'''
	import data_handlers 
	# print('sink',data_handlers.__sinkHandlers__.keys())
	# print('source',data_handlers.__sourceHandlers__.keys())
	return {	'sink':data_handlers.__sinkHandlers__,
				'source':data_handlers.__sourceHandlers__,
			}

def ensure_list(possible_list):
	''' ensures the value is a list. 
		basically if it's not currently a list
		wrap it up in a list'''

	if not isinstance(possible_list, list): return [possible_list]
	return possible_list
