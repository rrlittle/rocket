from Managers import sinkManager
from loggers import man_log
import utils
from Functions.function_api import DropRowException
from datetime import datetime

class ndar_snk(sinkManager):
    ''' ndar sink manager
    '''

    def __init__(self):
        super(ndar_snk, self).__init__()
        self.template_fields['id'] = 'ndar id'
        self.template_fields['col_name'] = 'ndar name'
        self.template_fields['col_range'] = 'ndar range'
        self.template_fields['mappers'] = 'mapping'
        self.template_fields['default'] = 'default value'
        self.template_fields['required'] = 'required'
        self.instrument_name = ""
        self.version = ""

    def parse_required(self, req, coldef):
        return req.lower() in ('true', 't')

    def parse_args(self, args, coldef):
        return args.split(',')

    def interview_date_write_formatter(self, dateobj, coldef):
        if isinstance(dateobj, self.NoDataError):
            return coldef.missing_vals

        if type(dateobj) == str:
            man_log.debug("date formatter catches a data string")
            return dateobj

        return dateobj.strftime('%m/%d/%Y')

    def ensure_row(self, datarow):
        man_log.debug("ENSURING DATA ROW %s" % datarow)
        for coldef, elem in datarow.items():

            if coldef.required:
                man_log.debug('row[%s](%s) is required' % (coldef, elem))
                if isinstance(elem, self.NoDataError):
                    # import ipdb; ipdb.set_trace()
                    man_log.critical("\n\n\nRAISING DROPROW")
                    raise DropRowException('%s' % elem)

    def set_instru_info(self, instru_name="", version=""):
        self.instrument_name = instru_name
        self.version = version

    def write_header(self, outfile):
        insr = self.instrument_name
        vers = self.version
        outwriter = utils.writer(outfile, delimiter=self.delimiter)
        outwriter.writerow([insr, vers])

    def parse_mappers(self, mappers, coldef):
        # This will check the syntax for the mappers, and do some clean up
        # The syntax should always be number seperated by comma. It's also possible to contain a pair of curly bracket,
        # used to indicate the number seperated by comma in the curly bracket should denote the column id in sink data source.
        import re
        if isinstance(mappers, str):
            mappers = mappers.replace(" ", "")

            if mappers == "":
                return "" # return the empty string

            # Use regular expression to match the string
            INTEGER = "[0-9]+"
            SEQUENCE_COMMA = "{number}(,{number})*".format(number = INTEGER)
            CURLY_ITEM = "\{%s\}" %SEQUENCE_COMMA
            ACCEPTABLE_FORMAT = "({number},)*{curly}?(,{number})*|{sequence}".format(number=INTEGER,
                                                                                     sequence=SEQUENCE_COMMA,
                                                                                     curly=CURLY_ITEM)
            ACCEPTABLE_FORMAT = "({number}|{curly})(,({number}|{curly}))*".format(number=INTEGER, curly=CURLY_ITEM)

            if re.fullmatch(ACCEPTABLE_FORMAT, mappers) is None:
                #user_error_log.log_mapping_error("Syntax for the mapper is wrong")
                raise Exception()
            return mappers

    def _auto_generate_file_path_(self):
        # gonna override it
        # I want to have the ability to use an automatically assigned name
        # The automatically generated name will be "apes01_12_18_2017_hour_cotwin_WTP.csv" so question becomes
        # how do I get cotwin or parent or twin? I would say ask: please enter respondent "cotwin, parent, twin"

        mm = self.mapping_manager
        if self.instrument_name == "" and self.version == "":
            return super()._auto_generate_file_path_()

        mm_name = type(mm).__name__
        instru_name = self.instrument_name
        time = datetime.now().strftime("%b_%d_%y_%H")

        # I need to add the respondent information in the template
        return super()._auto_generate_file_path_()

