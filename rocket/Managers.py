import utils
from __init__ import basedir, srcdatdir,sinkdatdir
from columns import Col, sinkCol, srcCol

class Manager(object):
	''' the generic manager ensuring all managers have basic 
		functionality like getting files and stuff
		we'll see what all we have later
	'''

	# for use when the template doesn't look as expected
	class TemplateError(Exception): pass

	def get_filepath(self, 
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

		fpath = utils.askopenfilename(
			title=title, 
			**kwargs)
		if fpath == '': 
			print('no %s file selected. quitting'%filetype)
			sys.exit()
		setattr(self,filetype, fpath)
		return fpath
	
	def __repr__(self): return str(self)
	def __str__(self): 
		if hasattr(self, '__name__'):return self.__name__
		else: return str(type(self).__name__)
	

class MetaManager(Manager):
	''' this is a class for the controller and mappingManager
		which need to know about
		source and sink managers. 

	'''
	def __init__(self, source=None, sink=None, 
		allow_instance=True, allow_class=True):
		''' if source and sink are instances asserts they 
			are instances of source and sink managers
			if they are classes, asserts they are subclasses
			of source or sink managers

			you can specify if you want to allow instances or classes
		'''
		# deal with source
		errstr = (	'if source must be a '
					'class referance class refd '
					'must be subclass of sourceManager. '
					'not %s')%source
		if allow_class and utils.isclass(source):
			assert issubclass(source, sourceManager), errstr 
			self.source = source()
		elif allow_instance: 
			assert isinstance(source, sourceManager), errstr
			self.source = source
		else: raise AssertionError('Unable to set self.source')

		# deal with source
		errstr = (	'if source must be a '
					'class referance class refd '
					'must be subclass of sinkManager. '
					'not %s')%sink
		if allow_class and utils.isclass(sink):
			assert issubclass(sink, sinkManager), errstr 
			self.sink = sink()
		elif allow_instance: 
			assert isinstance(sink, sinkManager), errstr
			self.sink = sink
		else: raise AssertionError('unable to set self.sink')


class ssManager(Manager):
	''' genetic class to give both soirce and sink 
		managers the same functions. 
		like __repr__ __str__ etc
	'''

	# for use when there is no data
	class NoDataError(Exception): pass

			
	def __init__(self, **kwargs):
		''' calls the super Manager init. then adds specific ss Manager stuff'''
		self.template_fields = utils.OrderedDict()
		self.template_fields['id'] = 'default_id_col'
		self.template_fields['col_name']='default_colname'


		self.col_defs = []  # ordered list of col objects in the data files
		# used to set what type of column to use to parse the template files

		self.col_archetype = Col # override this for different managers
			# srcCol and sinkCol behave slightly differently

	def __getitem__(self, k):
		''' return row, index only'''
		assert isinstance(k,int), 'ssManagers only support int indexing'
		if not hasattr(self, 'data'): 
			raise AttributeError(('%s has not been filled with data. run'
				' .initialize_data')%self)
			self.data[k]
	def __iter__(self): 
		if hasattr(self, 'data'): 
			self.row_pointer_for_iter = 0
			return self
		else: raise AttributeError

	def next(self): 
		if self.row_pointer_for_iter == len(self.data): raise StopIteration()
		tmp = self.data[0]
		self.row_pointer_for_iter += 1
		return tmp

	def getcolumn_defs(self, *collist):
		''' return the specified column objects from self.col_defs'''
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

	def load_template(self, templ_csv_reader):
		''' both managers need to be able to load a template
			and parse it to get what they need out of it. 
			however they need very different things. 
			so this just ensures both have them...

			they both need to load the template
		'''
		self.col_defs = []
		for tempmlate_row in templ_csv_reader:
			# use the column to parse the row as we would like it to be 
			c = self.col_archetype(self,template_row) 
			self.col_defs.append(c)


class sourceManager(ssManager):
	''' this should work as a source manager
		therefore it must implement all the things neccessary to 
		be a source manager. they should act in a reasonable way.
		so that any children will already hae most the things they need 
		and they can just change the few things they need
	'''
	defaultdatadir = srcdatdir

	def get_src_datfile(self):
		''' this function sets self.srcpath
			if this is already set it just passes it back
		''' 
		if hasattr(self, 'srcpath'): return self.srcpath
		else:
			self.srcpath = self.get_filepath(filetype='sourcedatafile',
				initialdir=self.defaultdatadir,
				title='select the source data file')
			return self.srcpath


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
	

	def get_file_outpath(self, allownew=False):
		''' this sets self.outpath
			this is called if the class doesn't know where to put the 
			outpath
			it can also be called in preperation

			allownew allows new files to be created
		'''
		if hasattr(self, 'outpath'): return self.outpath
		else:
			self.outpath = self.get_filepath(filetype='sinkdatafile',
				initialdir=self.defaultdatadir,
				title=('please select a new or exisiting file to '
					'save sink datafile to'))
		return self.outpath

	def initialize_data(self):
		''' if self.data exist then clear it
			create a new fresh self.data
		'''
		self.data = []

