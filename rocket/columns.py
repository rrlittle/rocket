import Managers


class Col(object):
	''' this represents one row from the template file. 
		it defines the parameters for a column from either the source or 
		the sink column.
		this will be extended by a sourceCol and sinkCol, which will each 
		implent further src/sink dependant functions
	'''

	# represents a data value that's missing
	class missingVal(object): pass

	def __init__(self, sshandler, template_row):
		'''all columns need
			- a handler. this asserts its an sshandler instance
			- column definitions
				i.e. the row from the template. source coluns and sink columns 
					require different things. but they all need:
					-  name
			'''
		
		#all columsn need to be aware of their handlers
		assert isinstance(sshandler, Managers.ssManager), ('handlers to colum objects '
			'must be children of ssManager')
		self.handler = sshandler

		self.template_row = template_row

	def load_attributes(self):
		''' loads all the attributes the handler knows about and 
			therefore needs
			this shoud be called after init, 
			but children of this should call it automatically in their init
		'''
		for field in self.handler.template_fields:
			self.load_attribute(field)

	def load_attribute(self, fieldkeyword):
		''' this sets the self.fieldkeyword_header attribute 
			& self.fieldkeyword attribute. 

			the fieldkeyword_header is the column name from the manager
			the fieldkeyword is the value from the template for this row
			
			this throws a templateError if it can't find either the keyword in
			this manager or the indicated column in the template
		'''
		try:
			header = fieldkeyword + '_header'
			setattr(self, header, self.handler.template_fields[fieldkeyword])
			# make the value available right now
			thisheader = getattr(self, header) 

			# for evey important field in a given hadler it should have a parse
			# function for that field called parse_'field'(fieldvalue)
			parser_name = 'parse_' + fieldkeyword 
			parser = getattr(self.handler, parser_name,  
				self.handler.default_parser)

			val = self.template_row[thisheader] # get raw value
			setattr(self, fieldkeyword, parser(val)) # save parsed value

		except Exception as e:
			raise self.handler.TemplateError(('Template not set up as expected.'
				' could not parse it. error occured: %s')%e)

	# the following are required to use this obj as keys for a dict
	# you can also access them by their column name 
	def __repr__(self): return self.col_name
	def __hash__(self): return self.col_name.__hash__()
	def __eq__(self, other): return self.col_name == other
	def __ne__(self,other): return not self.__eq__(other)

class srcCol(Col):
	''' this adds funcitonality to columns defining specifcally
		to sink cols.
	'''
	def __init__(self, sourcehandler, template_row, **kwargs):
		''' sourceCol requires some special things'''
		Col.__init__(self, sourcehandler, template_row)
		assert isinstance(self.handler, Managers.sourceManager), (
			'sinkCols require a source handler')
		
		self.load_attributes() # load all the handlers required attributes
		# from handler.template_fields

class sinkCol(Col):
	''' this adds funcitonality to columns defining specifcally
		to sink cols.
	'''

	def __init__(self, sinkhandler,template_row, **kwargs):
		'''sinkCol requires the handler to be a sinkManager'''
		Col.__init__(self, sinkhandler, template_row)
		assert isinstance(self.handler, Managers.sinkManager), (
			'sinkCols require a sink handler')

		self.load_attributes() # load all the handlers required attributes
		# from handler.template_fields
		

	def convert(self, src_datacol_zip):
		''' this will convert the src_data to a proper value for this column
			src_col_def may be a list or a src_data

			sets self.value and returns it. 
		'''
		unzip = zip(*src_datacol_zip) # list of sequences
		# change them to lsits so mutable
		srcdat = list(unzip[0]) 
		srccols = list(unzip[1]) 

		self.dat = self.func(*src_data, args=[arg for arg in self.args])
		return self.dat

