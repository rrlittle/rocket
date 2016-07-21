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
		self.template_fields['required'] = 'required'

	def parse_required(self, req, coldef):
		return req.lower() in ('true', 't')

<<<<<<< HEAD
	def interview_date_write_formatter(self, dateobj, coldef):
		if isinstance(dateobj, self.NoDataError):
			return coldef.missing_vals
		return dateobj.strftime('%m/%d/%Y')
=======
	def interview_date_write_formatter(self, dateobj):
		return dateobj.strftime('%m/%d/%Y')

	def ensure_row(self, datarow):
		for coldef, elem in datarow.items():
			if coldef.required: 
				if isinstance(elem, self.NoDataError):
					raise coldef.DropRowException('%s'%elem)
>>>>>>> added ensure row. currently not dropping rows we should be.... i.e. not all required rows are filled
