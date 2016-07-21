from Managers import sinkManager
from loggers import man_log
class ndar_snk(sinkManager):
	''' ndar sink manager
	'''
	def __init__(self):
		sinkManager.__init__(self)
		self.template_fields['id'] = 'ndar id'
		self.template_fields['col_name'] = 'ndar name'
		self.template_fields['col_range'] = 'ndar range'
		self.template_fields['mappers'] = 'mapping'
		self.template_fields['missing_vals'] = 'ndar missing value'
		self.template_fields['default'] = 'default value'


	def interview_date_write_formatter(self, dateobj, coldef):
		if isinstance(dateobj, self.NoDataError):
			return coldef.missing_vals
		return dateobj.strftime('%m/%d/%Y')