
# import some useful stuff
from inspect import getmembers, isclass, isfunction
import argparse
import tkinter
from tkinter.filedialog import askopenfilename
import csv
from os.path import join, abspath
import platform

# run som setup stuff
sytemName = platform.system()
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
