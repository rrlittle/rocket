import utils
from __init__ import basedir, srcdatdir,sinkdatdir
import columns
from loggers import man_log

class Manager(object):
	''' the generic manager ensuring all managers have basic 
		functionality like getting files and stuff
		we'll see what all we have later
	'''

	# for use when the template doesn't look as expected
	class TemplateError(Exception): pass

	def get_filepath(self, 
		save=False,
		title='open file', 
		filetype='file', 
		quit=True,
		allownew = True, 
		**kwargs):
		''' this is a generic function that can be extended 
		 	it simply gets a filepath and asserts it's not empty. 
		 	if it's empty the program quits unless quit is False. 
		 	when it will throw an error
		 	
		 	filetype is a string used for error messages and variable names 
			
		 	askopenfilename takes other kwargs as well you can look into
		 	all of them provided get passed on.
		 	- defaultextension - str expression for default extensions
		 	- others check out utils.askopenfilename docs for more 
			- initialdir - str path to where you would like to open 
		 	TODO: figure out how to disallow new files being made/ allow
		'''
		openfunc = None
		if save: openfunc = utils.asksaveasfilename
		else: openfunc = utils.askopenfilename

		# print(kwargs)
		fpath = openfunc(
			title=title,

			**kwargs)
		
		if fpath == '' or len(fpath) == 0: 
			print('no %s file selected. quitting'%filetype)
			utils.exit()
		setattr(self, filetype, fpath)
		man_log.debug('selected %s to be %s.'%(filetype, fpath))
		return fpath
	
	def __repr__(self): return str(self)
	def __str__(self): 
		if hasattr(self, '__name__'):return self.__name__
		else: return str(type(self).__name__)
			

class ssManager(Manager):
	''' genetic class to give both soirce and sink 
		managers the same functions. 
		like __repr__ __str__ etc
	'''

	# for use when there is no data
	class NoDataError(Exception): pass

	col_archetype = columns.Col # override this for different managers
		# srcCol and sinkCol behave slightly differently
			
	def __init__(self, **kwargs):
		''' calls the super Manager init. then adds specific ss Manager stuff'''
		self.template_fields = utils.OrderedDict()
		self.template_fields['id'] = 'default_id_col'
		self.template_fields['col_name']='default_colname'

		self.col_defs = []  # ordered list of col objects in the data files
		# used to set what type of column to use to parse the template files

	def __getitem__(self, k):
		''' return row, index only'''
		assert isinstance(k,int), 'ssManagers only support int indexing'
		if not hasattr(self, 'data'): 
			raise AttributeError(('%s has not been filled with data. run'
				' .initialize_data')%self)
		return self.data[k]
	def __iter__(self): 
		if hasattr(self, 'data'): 
			self.row_pointer_for_iter = 0
			return self
		else: raise AttributeError

	def __next__(self): 
		if self.row_pointer_for_iter == len(self.data): raise StopIteration()
		tmp = self.data[0]
		self.row_pointer_for_iter += 1
		return tmp

	def getcolumn_defs(self, *collist):
		''' return the specified column objects from self.col_defs'''
		#initialize ignore errors
		ignore_errors = True

		cols = [] # hold desired col instances
		for col in collist: # iterate the whole collist and save desired ones
			try:
				i = self.col_defs.index(col) # get the index of value
				cols.append(self.col_defs[i])
			except ValueError as e:
				errstr = ('while looking for column %s '
					'none found in %s')%(col,self)
				if ignore_errors: print(errstr)
				else: raise ValueError(errstr, e)
		return cols

	def load_template(self, templ_csv_file):
		''' both managers need to be able to load a template
			and parse it to get what they need out of it. 
			however they need very different things. 
			so this just ensures both have them...

			they both need to load the template
		'''
		templ_csv_reader = utils.DictReader(templ_csv_file)

		self.col_defs = []
		for template_row in templ_csv_reader:
			# use the column to parse the row as we would like it to be 
			c = self.col_archetype(self,template_row) 
			self.col_defs.append(c)

	def initialize_data(self):
		''' if self.data exist then clear it
			create a new fresh self.data
		'''
		self.data = []

	def default_parser(self, value): 
		''' just a simple parser if no other is defined'''
		print('value',value)
		try: return int(value)
		except: return str(value)

	
class sourceManager(ssManager):
	''' this should work as a source manager
		therefore it must implement all the things neccessary to 
		be a source manager. they should act in a reasonable way.
		so that any children will already hae most the things they need 
		and they can just change the few things they need
	'''
	defaultdatadir = srcdatdir
	col_archetype = columns.srcCol # override this for different managers
			# srcCol and sinkCol behave slightly differently
		
	col_archetype = columns.srcCol

	def __init__(self):
		''' adds sourceManager specific columns and things'''
		ssManager.__init__(self) # super the the init
		self.template_fields['id'] = 'source col id'
		self.template_fields['col_name']='source col name' 
		self.template_fields['col_range'] ='source col range'


	def get_src_datpath(self):
		''' this function sets self.srcpath
			if this is already set it just passes it back
		''' 
		if hasattr(self, 'srcpath'): return self.srcpath
		else:
			self.srcpath = self.get_filepath(filetype='srcpath',
				initialdir=self.defaultdatadir,
				title='select the source data file')
			return self.srcpath

	def load_data(self, clear_src=True):
		''' loads the source data file and stores it in self.data
			so that it can be iterated through easily
		'''
		man_log.debug('Loading source data into %s'%type(self).__name__)
		# if we want to clear the src
		if clear_src: self.initialize_data()

		# open file
		srcpath = self.get_src_datpath()
		srcfile = open(srcpath, errors='ignore')
		srcreader = utils.DictReader(srcfile)

		# assert the file has all the expected fields
		for col_name in self.col_defs: 
			print(col_name, srcreader.fieldnames)
			if col_name not in srcreader.fieldnames:
				raise self.TemplateError('expected column %s not '
					'found in source datafile, with fields: %s')%(
					col_name, list(srcreader.fieldnames))

		# load each row
		for datarow in srcreader:
			man_log.debug('parsing row %s'%datarow)
			row = utils.OrderedDict()
			for col in self.col_defs:
				man_log.debug('prasing %s from %s'%(col, datarow[col]))
				col_parser_name = 'parse_' + str(col)
				col_parser = getattr(self, col_parser_name, self.default_parser)
				row[col] = col_parser(datarow[col])
			self.data.append(row)
			
			
class sinkManager(ssManager):
	'''this should work as a sink manager
		therefore it must implement all the things neccessary to 
		be a sink manager. they should act in a reasonable way.
		so that any children will already hae most the things they need 
		and they can just change the few things they need
	'''

	# caller should drop the current row
	class DropRowException(Exception):pass 

	defaultdatadir = sinkdatdir
	col_archetype = columns.sinkCol # override this for different managers
			# srcCol and sinkCol behave slightly differently

	def __init__(self): 
		ssManager.__init__(self)
		self.template_fields['id'] = 'sink col id'
		self.template_fields['col_name'] = 'sink col name'
		self.template_fields['col_range'] = 'sink range'
		self.template_fields['mappers'] = 'sink mappers'
		self.template_fields['func'] = 'function'
		self.template_fields['args'] ='args'
	
	def get_file_outpath(self, allownew=False):
		''' this sets self.outpath
			this is called if the class doesn't know where to put the 
			outpath
			it can also be called in preperation

			allownew allows new files to be created
		'''
		if hasattr(self, 'outpath'): return self.outpath
		else:
			self.outpath = self.get_filepath(save=True, filetype='outpath',
				initialdir=self.defaultdatadir,
				title=('please select a new or exisiting file to '
					'save sink datafile to'))
		return self.outpath

	def write_outfile(self):
		''' writes self.data to a the outfile. which the user provides'''

		outpath = self.get_file_outpath()
		outfile = open(outpath, 'w')
		outwriter = utils.DictWriter(outfile, fieldnames = self.col_defs)
		outwriter.writeheader()
		for row in self.data:
			outwriter.writerow(row) 

		return outpath

	def add_row(self): self.data.append(utils.OrderedDict())	

	def parse_args