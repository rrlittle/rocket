from Managers import sourceManager, sinkManager, MetaManager
import utils
from __init__ import templatedir

class MappingManager(MetaManager):
	''' this class is responsible for implementing the 
		core algorithms governing the operation of
		the conversion routine. 
		it is also in charge of creation and parsing of 
		the template file. 
	'''
	tmeplate_seperator = ','

	def __init__(self, source=sourceManager(), sink = sinkManager()):
		''' it's imperative that this instance know about
			a source and sink manager. they are the providers 
			for all the information in the raw files. 
			this should never be using raw info
		'''
		MetaManager.__init__(self, source=source, sink=sink, allow_class=False)
		# sets self.source, self.sink to be instatiated things


	def get_template(self, allownew=False):
		''' this gets the filepath to a file. which is assumed to be 
			a template file. we will rely on source sink handlers for error
			checking when they load it in

			allownew should decide if it's okay to allow a new file or not
		'''

		tmppath = self.get_filepath(title='tenplate',
			initialdir=templatedir,
			filetype='templates',
			allownew = allownew)

		self.templ_path = tmppath
		return self.templ_path

	def parse_template(self):
		''' this function utilises self.sink and self.source
			to parse the template file. each managaer will 
			take the columns they know about. 
		'''
		for handler in [self.source, self.sink]:
			with open(self.templ_path, errors='replace') as templfile:
				templreader = utils.DictReader(templfile)
				handler.load_template(templreader)

	def convert(self, clear_sink=True):
		''' this function implements the core algorithm of rocket.
			this sets up the core behaviour of the template files. 
			basically it applies the function specified with the 
			arguments provided to the columns in the source
			and save the returning value in sink. 

			the goal here is to fill up sink.data in prep for sink.write
		'''
		if clear_sink: # if sink is not already initialized		
			self.sink.initialize_data() # clear any data in sink

		self.src.load_data() # ensure src has data

		for i,row in enumerate(self.src):
			self.sink.add_row()
			for sinkcol in self.sink.cols:
				try:
					srcdat = self.src.get(sinkcol.mappers)
					sinkdat = self.sink.convert(srcdat, 
						src_missing_vals=self.src.missing_values)
					self.sink[i][sinkcol] = sinkdat
				except sinkManager.DropRowException:
					self.sink.drop_row()
		return self.sink.data





