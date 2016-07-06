import tkinter.filedialog as filedialog
from os import getcwd
from os.path import join, abspath
import sys
import csv


class Manager(object):
	def get_filepath(self, 
		title='open file', 
		filetype='file', 
		initialdir='',
		defaultextension='csv', 
		**kwargs):
		''' this is a generic function that can be extended 
		 	it simply gets a filepath and asserts it's not empty. 
		 	if it's empty the program quits.
		 	filetype is a string used for error messages and variable names 

		 	askopenfilename takes other kwargs as well you can look into
		 	all of them provided get passed on.
		'''

		print('in get_filepath opening', abspath(initialdir))
		fpath = filedialog.askopenfilename(title=title, 
			initialdir=join(getcwd(), initialdir),
			defaultextension=defaultextension,
			**kwargs)
		if fpath == '': 
			print('no %s file selected. quitting'%filetype)
			sys.exit()
		setattr(self,filetype, fpath)
		return fpath
	

class ssManager(Manager): 
	'''
	'''
	def __init__(self):
		self.handlername = 'default' # what is the name of this handler

		self.defaultschemedir = ''
		self.defaultdatadir = ''

		self.fieldnames={ # bare bones that should always be in every handler
			'name_col': 'name',
			'missing_val_col': 'missing value',
			'range_col': 'range',
		}
		

	# this will load a schema into the data handler. 
	# in general we don't really know how to do it 
	# so this will just load a file
	# that you can use in child classes
	# . you should really overwrite this in the real handlers
	# because they are all going to need that. 
	def load_schema(self, *args, 
		title='please select a scheme file for this handler',
		filetype='schema', 
		initialdir='',
		**kwargs):
		return self.get_filepath(title=title, filetype=filetype, 
			initialdir=initialdir)
	
	def load_template(self, template_file):
		''' this parses all the things from the template_file
			this thing knows about '''
		raise NotImplementedError(("load_template not implemented",
			" for this manager"))	


class sourceManager(ssManager):
	'''
	'''
	def __init__(self):
		ssManager.__init__(self)
		
		self.defaultschemedir = 'source_schemes'
		self.defaultdatadir = 'source_datafiles'
		
		self.handlername = 'generic source handler'

		self.fieldnames['id_col'] = 'id'
		self.fieldnames['name_col'] = 'source name'
		self.fieldnames['missing_val_col'] = 'source missing value'

	# this function gets the path to the source datafile.
	# you can assert that it is in the correct format if you wish in 
	# subclasses. 
	def get_data_path(self):
		if hasattr(self, 'srcpath'): return self.srcpath
		else:
			self.srcpath = self.get_filepath(filetype='sourcedatafile',
				initialdir=self.defaultdatadir,
				title='select the source data file')
			return self.srcpath

	def parse_datasource(self, path_to_source):
		pass


class sinkManager(ssManager):
	'''
	Option: you can add Size, Element Description
	'''
	def __init__(self):
		ssManager.__init__(self)
		
		self.defaultschemedir = 'sink_schemes'
		self.defaultdatadir = 'sink_datafiles'
		self.handlername = 'generic sink handler'

		self.fieldnames['mapping_id_col'] = 'mapping id'
		self.fieldnames['function'] = 'function'
		self.fieldnames['args'] = 'args'
		self.fieldnames['name_col'] = 'sink name'
		self.fieldnames['missing_val_col'] = 'sink missing value'
		self.fieldnames['default_val'] = 'default value'

	# this function prompts the user to enter a valid 
	# path to a new file, or one to overwrite that 
	# will be where the sink table gets saved when
	# it's all over. 
	def get_file_outpath(self):
		if hasattr(self, 'outpath'): return self.outpath
		else:
			self.outpath = self.get_filepath(filetype='sinkdatafile',
				initialdir=self.defaultdatadir,
				title=('please select a new or exisiting file to '
					'save sink datafile to'))
		return self.outpath

	# writes the data in the form of 
	# headers
	# data lines
	# to the file passed.
	# this can be extended  
	def write_outfile(self, data, sinkpath=None, outfile=None, mode='w'):
		if outfile is None:
			outfile = open(sinkpath, mode, newline='')

		write_fieldnames = [];
		for column in data[0]:
			write_fieldnames.append(column.col_name)

		writer = csv.DictWriter(outfile, fieldnames = write_fieldnames,
				extrasaction='ignore')
		writer.writeheader()
		f = open('oggaadaboogida', 'w')
		for row in data:
			row = {c.col_name:c.data for c in row}
			f.write('writing : %s\n'%row)
			writer.writerow(row)
