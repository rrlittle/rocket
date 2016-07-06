from ssManagers import sourceManager, sinkManager, Manager
import functions

class MappingManager(Manager):

	def __init__(self, src=sourceManager(), sink=sinkManager()):
		self.src = src
		self.sink = sink

	def load_template(self, template_path=None, src_data_path=None):
		''' loads an existing template_file and asserts it's correctness
			then loads columns into the source and sink managers
			in preparation for self.mapping
		'''
		if template_path is None:
			template_path = self.get_filepath(title='load template',
				filetype='mapping files',
				initialdir='mapping_files',
				defaultextension='csv')
		template_file = open(template_path)
		# for now don't assert correctness. 
		# that just complicates it

		# have src and sink fill up on their respective information
		self.src.load_template(template_file)
		template_file.seek(0)
		self.sink.load_template(template_file)

	def mapping(self, clear_sink=True):
		''' does the mapping between the src schema and the 
			sink schema '''
		if clear_sink: # if sink is not already initialized		
			self.sink.initialize_data() # clear any data in sink

		self.src.load_data() # ensure src has data

		for i,row in enumerate(self.src):
			self.sink.add_row()
			for sinkcol in self.sink.cols:
				try:
					srcdat = self.src.get(self.sink.mappers)
					sinkdat = self.sink.convert(srcdat, 
						src_missing_vals=self.src.missing_values)
					self.sink[i][sinkcol] = sinkdat
				except sinkManager.DropRowException:
					self.sink.drop_row()

		return self.sink.data
