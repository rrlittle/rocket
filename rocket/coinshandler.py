from Managers import sourceManager

class coinshandler(sourceManager):

	def __init__ (self, **kwargs):
		super(coinshandler, self).__init__(**kwargs):
		self.template_fields['id'] = 'coins col id'
		self.template_fields['col_name'] = 'coins col name'
		self.template_fields['col_range'] = 'coins col range'

	def  parse_assessment_date(self, data):
    	assessment_dateformat = "%m/%d/%Y %H:%M"
    	return datetime(data, assessment_dateformat)
