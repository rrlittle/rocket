from Managers import sinkManager
from loggers import man_log
import utils


class ndar_snk(sinkManager):
    ''' ndar sink manager
    '''

    def __init__(self):
        sinkManager.__init__(self)
        self.template_fields['id'] = 'ndar id'
        self.template_fields['col_name'] = 'ndar name'
        self.template_fields['col_range'] = 'ndar range'
        self.template_fields['mappers'] = 'mapping'
        self.template_fields['default'] = 'default value'
        self.template_fields['required'] = 'required'

    def parse_required(self, req, coldef):
        return req.lower() in ('true', 't')

    def interview_date_write_formatter(self, dateobj, coldef):
        if isinstance(dateobj, self.NoDataError):
            return coldef.missing_vals
        return dateobj.strftime('%m/%d/%Y')

    def ensure_row(self, datarow):
        man_log.debug("ENSURING DATA ROW %s" % datarow)
        for coldef, elem in datarow.items():
            if coldef.required:
                man_log.debug('row[%s](%s) is required' % (coldef, elem))
                if isinstance(elem, self.NoDataError):
                    # import ipdb; ipdb.set_trace()
                    man_log.critical("\n\n\nRAISING DROPROW")
                    raise self.DropRowException('%s' % elem)

    def set_instru_info(self, instru_name="", version=""):
        self.instrument_name = instru_name
        self.version = version

    def write_header(self, outfile):

        insr = self.instrument_name
        vers = self.version
        outwriter = utils.writer(outfile, delimiter=self.delimiter)
        outwriter.writerow([insr, vers])

        pass;
