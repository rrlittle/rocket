from Managers import ssManager, sinkManager, sourceManager

class Col(object):
	''' this represents one row from the template file. 
		it defines the parameters for a column from either the source or 
		the sink column.
		this will be extended by a sourceCol and sinkCol, which will each 
		implent further src/sink dependant functions
	'''
	class missingVal(object):
		''' represents a data value that's missing'''
		pass

	def __init__(self, sshandler):
		'''all columns need
			- a handler. this asserts its an sshandler instance
			'''
		
		#all columsn need to be aware of their handlers
		assert isinstance(sshandler, ssManager), ('handlers to colum objects '
			'must be children of ssManager')
		self.handler = sshandler
	

class srcCol(Col):
	''' this adds funcitonality to columns defining specifcally
		to sink cols.
	'''
	def __init__(self, sourcehandler, **kwargs):
		''' sourceCol requires some special things'''
		Col.__init__(self, sourcehandler)
		assert isinstance(self.handler, sourceManager), ('sinkCols require a',
			' source handler')
		# set missingVals


class sinkCol(Col):
	''' this adds funcitonality to columns defining specifcally
		to sink cols.
	'''
	def __init__(self, sinkhandler,**kwargs):
		'''sinkCol requires the handler to be a sinkManager'''
		Col.__init__(self, sinkhandler)
		assert isinstance(self.handler, sinkManager), ('sinkCols require a',
			' sink handler')
		# set self.func
		# set self.args


	def convert(self, src_datacol_zip):
		''' this will convert the src_data to a proper value for this column
			src_col_def may be a list or a src_data

			sets self.value and returns it. 
		'''
		unzip = zip(*src_datacol_zip) # list of sequences
		# change them to lsits so mutable
		srcdat = list(unzip[0]) 
		srccols = list(unzip[1]) 

		for i in range(len(src_datacol_zip)): 
			if srcdat[i] in srccols[i].missingVals:
				srcdat[i] = self.missingVal()

		self.dat = self.func(*src_data, args=*self.args)
		return self.dat
