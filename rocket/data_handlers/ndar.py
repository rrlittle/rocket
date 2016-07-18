from Managers import sinkManager

class ndar_snk(sinkManager):
	''' ndar sink manager
	'''
	def __init__(self):
		sinkManager.__init__(self)
		self.template_fields['id'] = 'ndar id'
		self.template_fields['col_name'] = 'ndar name'
		self.template_fields['col_range'] = 'ndar range'
		self.template_fields['mappers'] = 'mapping'


