from Managers import sourceManager
import utils

class coins_src(sourceManager):
    ''' coins source
    '''
    delimiter = '\t'

    def __init__(self):
    	sourceManager.__init__(self)
    	self.template_fields['id'] = 'coins id'
    	self.template_fields['col_name'] = 'coins name'
    	self.template_fields['col_range'] = 'coins range'
    	self.template_fields['missing_vals'] = 'coins missing value'
    	print(self.template_fields)

    def parse_assessment_date(self, assessment_date, coldef):
    	assessment_dateformat = "%m/%d/%Y %H:%M"
    	assessment_date = utils.datetime.strptime(assessment_date,
    		assessment_dateformat)
    	return assessment_date

    