from Managers import sourceManager
import utils

dateformat_candidates =[
    "%m/%d/%Y %H:%M",
    "%m/%d/%y %H:%M",
    "%m-%d-%Y %I:%M:%S %p",
    "%m/%d/%Y"
    ]

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

    def parse_assessment_date(self, assessment_date, coldef):
        '''
        Given an assessment_date,
        :param assessment_date:
        :param coldef:
        :return:
        '''
        for dateformat in dateformat_candidates:

            try:
                assessment_date = utils.datetime.strptime(assessment_date,
                    dateformat)
                return assessment_date
            except Exception as e:
                pass
        raise ValueError("The assessment_date in data file is not matched in any acceptable date format in rocket")


    def parse_date(self,date, coldef):
        for dateformat in dateformat_candidates:
            try:
                assessment_date = utils.datetime.strptime(date,
                    dateformat)
                return assessment_date
            except Exception as e:
                pass

        raise ValueError("The assessment_date in data file is not matched in any acceptable date format in rocket")
