from inspect import getmembers, isclass, isfunction
import argparse
import tkinter
from tkinter.filedialog import askopenfilename
import csv
from os.path import join, abspath

tkinter.Tk().withdraw()

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
