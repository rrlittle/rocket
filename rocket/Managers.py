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
	class NoDataError(Exception): 
		'''Add things to support indexing and splat'''
		def __iter__(self):return iter([])
		def __getitem__(self, item): return self
		

	delimiter = ','
	col_archetype = columns.Col # override this for different managers
	# srcCol and sinkCol behave slightly differently
			
	def __init__(self, **kwargs):
		''' calls the super Manager init. then adds specific ss Manager stuff'''
		self.template_fields = utils.OrderedDict()
		self.template_fields['id'] = 'default_id_col'
		self.template_fields['col_name']='default_colname'

		self.col_defs = [] 
		self.row_pointer_for_iter = 0 
		 # ordered list of col objects in the data files
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
		tmp = self.data[self.row_pointer_for_iter]
		self.row_pointer_for_iter += 1


		return tmp

	def getcolumn_defs(self, *collist):
		''' collist is: tuple of string names that are the 
				column headers
		return the specified column objects from self.col_defs'''
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
				if ignore_errors: pass #print(errstr)
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
		for rid, template_row in enumerate(templ_csv_reader):
			# use the column to parse the row as we would like it to be 
			try:
				col = self.col_archetype(self,template_row)
				self.col_defs.append(col) 
				man_log.info(('Loading template for %s: row %s. '
					'created column %s')%(self, rid, col))
			except self.col_archetype.BadColErr as e:
				man_log.info(('%s column not created '
					'beacause %s')%(self.col_archetype.__name__,e))

	def initialize_data(self):
		''' if self.data exist then clear it
			create a new fresh self.data
		'''
		self.data = []


	def default_template_parser(self, value, coldef):
		''' unifies how we parse the template fields. 
			empty fields are always filled with NoDataErrors
			then will be a string. 
		'''
		if value == '': return self.NoDataError('template fld empty')
		else: return str(value) 

	def default_parser(self, value, coldef): 
		''' just a simple parser if no other is defined
			used when parsing the template?'''
		man_log.debug('parsing [%s] from (%s)'%(coldef, value))
		missing =[] # updated below if exists

		if hasattr(coldef, 'missing_vals'): 
			man_log.debug('checking if %s in missing vals: %s'%(value, 
				coldef.missing_vals))
			missing = coldef.missing_vals.split(",")

		if hasattr(coldef, 'missing_vals') and value in missing:
			man_log.debug('replacing row[%s](%s) with NoData'%(coldef, value))
			return self.NoDataError(('value %s identified as a missing '
				'value for col %s')%(value, coldef))
		man_log.debug('parse result is (%s)'%value)
		return str(value)


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


	class BadSourceRowErr(Exception):
		pass

	def __init__(self):
		''' adds sourceManager specific columns and things'''
		ssManager.__init__(self) # super the the init
		self.template_fields['id'] = 'source col id'
		self.template_fields['col_name']='source col name' 
		self.template_fields['col_range'] ='source col range'
		self.template_fields['missing_vals'] = 'source missing values'

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

			NOTE. IF datafile lives on a server through a vpn. this runs
			REALLY REALLY SLOWLY...
			we should pull the file and use readlines to save them to 
			memory and close the file to speed things up. rather than querying
			every time.
		'''
		man_log.info('Loading source data into %s'%type(self).__name__)
		# if we want to clear the src
		if clear_src: self.initialize_data()

		# open file
		srcpath = self.get_src_datpath()
		srcfile = open(srcpath, errors='ignore')
		srcreader = utils.DictReader(srcfile, delimiter=self.delimiter)

		# assert the file has all the expected fields
		man_log.debug('expected fieldnames: %s'%self.col_defs)
		for col_name in self.col_defs: 
			if col_name not in srcreader.fieldnames:
				raise self.TemplateError(('expected column %s not '
					'found in source datafile, with fields: %s')%(
					col_name, list(srcreader.fieldnames)))

		# load each row
		for rowid, datarow in enumerate(srcreader):
			man_log.info('loading row %s'%rowid)
			man_log.debug('parsing row %s : %s'%(rowid, datarow))
			row = utils.OrderedDict()
			for col in self.col_defs:
				try:
					col_parser_name = 'parse_' + str(col)
					man_log.debug('parsing %s from %s using %s'%(col,
					 datarow[col], col_parser_name))
					col_parser = getattr(self, col_parser_name, 
						self.default_parser)
					row[col] = col_parser(datarow[col.col_name], col)
				except Exception as e:
					man_log.debug('Exception while parsing %s: %s'%(col, e))
					row[col] = self.NoDataError('%s'%e)
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
		self.template_fields['default'] = 'sink default value'
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

		outfile = None
		outpath = self.get_file_outpath()

		
		try:
			outfile = open(outpath, 'w', newline = "")
		except PermissionError as e:
			input(('%s was not opened successfully. perhaps it is open. '
				'close it and hit neter to cont')%outpath)
			outfile = open(outpath, 'w', newline = "")


		self.write_header(outfile)
		outwriter = utils.DictWriter(outfile, fieldnames = self.col_defs)	
		outwriter.writeheader()
		for rowid,row in enumerate(self.data):
			for coldef, elem in row.items():
				if isinstance(elem, self.NoDataError): # print the default value. 
					elem = ''
				formatter = getattr(self, coldef+'_write_formatter', 
						self.default_write_formatter)
				man_log.debug('trying formatter %s'%(
							coldef+'_write_formatter'))
				man_log.debug('formatting row[%s][%s](%s) with %s'%(rowid,
						coldef,row[coldef], formatter.__name__))
				row[coldef] = formatter(row[coldef], coldef)
				man_log.debug('writing row[%s][%s] is %s'%(rowid, coldef, 
						row[coldef]))
			outwriter.writerow(row) 

		return outpath

	def write_header(self, outfile):
		''' this is a hook for handler to write headers on the 
			outfile
		'''
		pass

	def add_row(self): self.data.append(utils.OrderedDict())    
	def drop_row(self): self.data.pop()

	def default_write_formatter(self, value, coldef):
		''' this is the default output formatter. you can overwrite this 
			in your handlers to format any specific columns however you like. 
			you will need to know what you expect and what to output. 
			which really depends on the column.

			name the function {colname}_write_formatter.
		'''
		if isinstance(value, self.NoDataError):
			return coldef.default
		return str(value) 

	def ensure_row(self, datarow):
		''' default ensure row function always accepts rows. 
			you should override this for your handlers. using whatever 
			tepmlate fields you would like or do whatever you would like. 
			
			raise a coldef.DropRowException if you would like to 
			drop the row. otherwise return None
		'''
		pass
