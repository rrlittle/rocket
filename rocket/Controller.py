from Managers import sourceManager, sinkManager, MetaManager
from MappingManager import MappingManager
import utils 

class controller(MetaManager):
	''' this class is aware of all three types of managers.
		source sink and mapping. 
		this takes the responsibility of orchestrating the whole 
		mapping from sinkt to source. 
	'''
	def __init__(self, source=sourceManager, sink=sinkManager):
		''' this initializes the controller
			it takes a referance to a sourceManager and a sinkManager
			class. they shold be classes not instances. 
			I will call them thank you very much. 
		''' 
		MetaManager.__init__(self, source=source, sink=sink)
		self.mapper = MappingManager(source=self.source, sink=self.sink)
		
	def make_template(self):
		''' this makes a new template. 
			it will require both the source and sink schemas
			as they will be used by the mapping manager to 
			create the template
		'''
		pass
	def do_convert(self, template_path= None):
		''' this takes an existing template and asks the 
			mapping manager to parse it using the source and sink
			managers
		'''
		self.sink.get_outfile(allownew=True) # ensure sink knows where its goin
		self.source.get_src_datfile() # ensure source knows where it's comin
		self.mapper.get_template() # ensure mapper has a template

		# parse the template, setting up src and sink
		self.mapper.parse_tempate() 

		# fill sink with converted data from source
		self.mapper.convert()

		return self.sink.write_outfile()