import utils
from __init__ import basedir, srcdatdir,sinkdatdir

class Manager(object):
	''' the generic manager ensuring all managers have basic 
		functionality like getting files and stuff
		we'll see what all we have later
	'''
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
					'must be subclass of sourceManager')
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
					'must be subclass of sourceManager')
		if allow_class and utils.isclass(source):
			assert issubclass(source, sourceManager), errstr 
			self.source = source()
		elif allow_instance: 
			assert isinstance(source, sourceManager), errstr
			self.source = source
		else: raise AssertionError('unable to set self.sink')

class ssManager(Manager):pass
class sourceManager(ssManager):
	''' this should work as a wource manager
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
	defaultdatadir = sinkdatdir
	def get_file_outpath(self):
		''' this sets self.outpath
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
			create a new fresj self.data
		'''
