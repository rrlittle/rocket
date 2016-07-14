from MappingManager import sinkManager
from datetime import datetime

class ndarhandlers(sinkManager):
	def __init__(self, **kwargs):
		super(sinkManager,self).__init__(**kwargs)
		self.template_fields['id'] = 'ndar col id'
		self.template_fields['col_name'] = 'ndar col name'
		self.template_fields['col_range'] = 'ndar col range'
		self.template_fields['mappers'] = 'mappers'
		self.template_fields['func'] = 'function'
		self.template_fields['args'] = 'args'
		self.template_fields['missing_value'] = 'ndar missing value'

