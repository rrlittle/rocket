from Managers import sourceManager, sinkManager, Manager
import utils
from __init__ import templatedir, templ_delimiter, secretdir
from loggers import map_log
import ipdb

class MappingManager(Manager):
	''' this class is responsible for implementing the 
		core algorithms governing the operation of
		the conversion routine. 
		it is also in charge of creation and parsing of 
		the template file. 
	'''
	delimiter = templ_delimiter
	def __init__(self, source=sourceManager, sink = sinkManager):
		''' it's imperative that this instance know about
			a source and sink manager. they are the providers 
			for all the information in the raw files. 
			this should never be using raw info
		'''

		# deal with source
		errstr = (	'if source must be a '
					'class referance class refd '
					'must be subclass of sourceManager. '
					'not %s')%source
		assert issubclass(source, sourceManager), errstr 
		self.source = source()
		
		# deal with sink
		errstr = (	'if source must be a '
					'class referance class refd '
					'must be subclass of sinkManager. '
					'not %s')%sink
		assert issubclass(sink, sinkManager), errstr 
		self.sink = sink()
		
		
		self.check_valid_src_sink_combo()

		# make the functions of each available via utils
		# check for naming conflicts
		self.globalfuncs = self.load_functions()

		# pass functions down to sink maanager for the sinkcolumns to use
		setattr(self.sink, 'globalfuncs', self.globalfuncs)

	def load_functions(self):
		''' must be overwritten by Mapping manager subclasses. 
			in order to include functions that are aware of both 
			source and sink schemes.
			It should be a dictionary looks like {"mean":{"ref": mean }  }, mean
			is the reference of the mean function
		'''
		return {}

	def get_template(self, title='Template', allownew=False, save=False):
		''' this gets the filepath to a file. which is assumed to be 
			a template file. we will rely on source sink handlers for error
			checking when they load it in

			allownew should decide if it's okay to allow a new file or not
		'''

		tmppath = self.get_filepath(title=title,
			initialdir=templatedir,
			save=save,
			filetype='templates',
			allownew = allownew)

		self.templ_path = tmppath
		return self.templ_path

	def parse_template(self):
		''' this function utilises self.sink and self.source
			to parse the template file. each managaer will 
			take the columns they know about. 
		'''
		templ_path = None
		if hasattr(self, 'templ_path'):
			templ_path = self.templ_path
		else:
			templ_path = self.get_template()
	
		for handler in [self.source, self.sink]:
			map_log.debug(('loading template into '
				'handler %s')%type(handler).__name__)
			with open(templ_path, errors='replace') as templfile:
				handler.load_template(templfile)

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
				' sink handler template_fieldnames. pleae modify these fields '
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

		map_log.critical('loading data')
		# ipdb.set_trace()
		self.source.load_data() # ensure src has data


		for rowid,srcrow in enumerate(self.source): 
			self.sink.add_row() # we want to fill in a new row

			try:
				# go through all the columns defined in the template
				for sinkcoldef in self.sink.col_defs: 
					try:
						# if rowid >= 25:
						#	ipdb.set_trace()
						# sinkcol maps from the id to sourceColMappers 
						sinkcoldef.map_src(srcrow)
						# get col objs from src

						mapperslist = sinkcoldef.mappers 
							# src cols required to compute the sink value
						

						if not isinstance(mapperslist, self.sink.NoDataError):
							srccols = self.source.getcolumn_defs(*mapperslist) 
							# list of columns in the source datafile we need to grab
				
							# get the data					
							srcdat = [srcrow[col.col_name] for col in srccols]
							# list of data values from src datafile
							# zip the data with it's defining object
							# needed for sinkcol.convert
							src_datcol_zip = zip(srcdat, srccols)
							
							# convert it to the sink value
							sinkdat = sinkcoldef.convert(src_datcol_zip)

							#print('output:',sinkdat)
							# save the sink value to the last row
							self.sink[-1][sinkcoldef] = sinkdat

						else:
							self.sink[-1][sinkcoldef] = sinkcoldef.default
							

					except sinkManager.DropRowException as e:
						raise e
					except Exception as e:
						map_log.error(('A not drop row exception happen when'
										'processing data in a row: %s')%e)
						self.sink[-1][sinkcoldef] = sinkcoldef.default
						continue;

				# after the row is done use ensure row
				self.sink.ensure_row(self.sink.data[-1]) # raise drop row exception if row not right

			except sinkManager.DropRowException as e:
				# drop the row if it should't be included in the dataset
				map_log.error(('not including source row %s in sink: err'
									' at %s (%s)')%(rowid, sinkcoldef, e))
				self.sink.drop_row()
			except Exception as e:
				map_log.error('not droprow exception: %s'%e)
				continue


		map_log.critical('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nDONE CONVERSION')
		
		return self.sink.data

	def get_mapperids(self,mapper_string):
		#print('################### %s'%mapper_string)
		mapper_ids = []
		if '::' not in mapper_string:
			return mapper_string.split(',')

		if '::' in mapper_string:
			mapper_temp = mapper_string.split('::')
			try:
				start = int(min(mapper_temp))
				end = int(max(mapper_temp))
				mapper_ids = [str(x) for x in range(start, end+1)]
				return mapper_ids
			except ValueError:
				raise sinkManager.DropRowException

	def make_template(self):
		''' leverages the sink and source handlers to make the template
			file. 
			
			writes handler documentation as top header using 
			self.template_header
			
			then calls sink handler to write it's documentation as the second 
			header

			then calls source header to write it's documentation as the third 
			header

			then wtites global funcs with their documentation as the 4th header

			finally uses sink.get_template_fields and source.get_template_fields
			to populate the final template header.

			then calls sink and source.populate_template to populate the 
			template.

			for a specific mapping manager include a list of strings to be
			included as the header for that thing. 
		'''
			
		templ_path = None
		if hasattr(self, 'templ_path'):
			templ_path = self.templ_path
		else:
			templ_path = self.get_template(title='Select a template file', 
				save=True, allownew=True)
		
		def handle_tmeplate_err(errstr,err):
			map_log.err(('%s... Template field getting deleted and '
				'rocket quitting. Error: %s')%(errstr,err))
			templfile.close()
			utils.remove(templ_path)
			utils.exit(1)

		templfile = open(templ_path, 'w')
		self.header_lines = 0
		try:
			self.header_lines += self.write_templ_header(templfile)
			self.header_lines += self.sink.write_templ_header(templfile)
			self.header_lines += self.source.write_templ_header(templfile)
		except Exception as e:
			handle_tmeplate_err('error while writing headers', e)

		# the template fields for each handler are defined upon initialization 
		# of the handlers. they are defined in the code and extended for each 
		# custom handler if they so choose. 
		# they will be in order of definition in the __init__
		srctemplatefields = list(self.source.template_fields.values())
		sinktemplatefields = list(self.sink.template_fields.values())
		templatefields = srctemplateheaders + sinktemplateheaders
		
		wr = utils.writer(templfile, delimiter=self.delimiter)
		wr.writerow(templatefields)
		self.header_lines += 1

		try:
			# write the column defs for sink
			self.sink.populate_template(templfile, templatefields) 
			templfile.close()
		except Exception as e:
			handle_tmeplate_err('error while populating sink columns', e)
		
		try:
			# allow rewrite of rows starting just below the headers
			templfile = open(templ_path, 'w+')
			# skip to below headers
			for i in range(self.header_lines): 
				templfile.readline() 
			# write the column defs for source
			self.source.populate_template(templfile, templatefields)
			templfile.close() # done with template. wait for user input
		except Exception as e:
			handle_tmeplate_err('error while populating sink columns', e)

		map_log.debug('Template created')
		inp = input(('\n\nThe template file has been written. \n'
			'Please hit enter when you are done with the file and you will'
			' continue to the conversion if you have selected both options\n'
			'enter "q" if you would like to quit now and fill the template at ' 
			'another time\n>>'))

		if inp == 'q': 
			map_log.critical('User elected to quit after template was created')
			utils.exit()

		return templ_path


