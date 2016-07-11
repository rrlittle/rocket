from Managers import sourceManager, sinkManager, MetaManager
import utils
from __init__ import templatedir
from loggers import map_log

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
		templ_path = self.get_template()
		for handler in [self.source, self.sink]:
			with open(templ_path, errors='replace') as templfile:
				templreader = utils.DictReader(templfile)
				handler.load_template(templreader)

	def check_valid_src_sink_combo(self):
		''' ensures that src and sink do not have colliding fieldnames
			if they do there will be an issue with parsing and creating the 
			template all the headers must template headers must be unique'''
		# generate list of all the headers
		srctemplateheaders = list(self.source.template_fields.values())
		sinktemplateheaders = list(self.sink.template_fields.values())
		templateheaders = srctemplateheaders + sinktemplateheaders
		# find collisions
		collisions = []
		tmp = []
		for header in templateheaders:
			if header not in tmp: tmp.append(header)
			else: collisions.append(header)
		# and raise error if there are any collisions
		if len(collisions != 0): 
			raise self.TemplateError(('collisions detected in src and'
				' sink hndler template_fieldnames. pleae modify these fields '
				'to ensure unique headers: %s')%collisions) 

	def convert(self, clear_sink=True):
		''' this function implements the core algorithm of rocket.
			this sets up the core behaviour of the template files. 
			basically it applies the function specified with the 
			arguments provided to the columns in the source
			and save the returning value in sink. 

			the goal here is to fill up sink.data in prep for sink.write
		'''
		# import ipdb; ipdb.set_trace()
		
		if clear_sink: # if sink is not already initialized		
			self.sink.initialize_data() # clear any data in sink

		map_log.debug('loading data')
		self.source.load_data() # ensure src has data

		for srcrow in self.source: 
			self.sink.add_row() # we want to fill in a new row

			# go through all the columns defined in the template
			for sinkcoldef in self.sink.col_defs: 
				try:
					# get col objs from src
					mapperslist = sinkcoldef.mappers 
						# src cols required to compute the sink value
					srccols = self.source.getcolumn_defs(*mapperslist) 
						# list of columns in the source datafile we need to grab
					
					# get the data					
					srcdat = [srcrow[col] for col in srccols]
						# list of data values from src datafile
					
					# zip the data with it's defining object
					# needed for sinkcol.convert
					src_datcol_zip = zip(srcdat, srccols)
					
					# convert it to the sink value
					sinkcol.convert(src_datcol_zip)

					# save the sink value to the last row
					self.sink[-1][sinkcoldef] = sinkdat
				except sinkManager.DropRowException: 
					# drop the row if it should't be included in the dataset
					self.sink.drop_row()
		return self.sink.data






