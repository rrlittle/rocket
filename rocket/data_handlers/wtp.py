from Managers import sourceManager, sinkManager
import utils
import re 
from loggers import man_log
import pyodbc
import enum


class TableType(enum.Enum):
    FamilyTable = 1
    TwinTable = 2


class WtpSource(sourceManager):
    ''' this is used to pull data and stuff from the wtp database 
        or yaml files defining the instruments and things 
    '''

    def __init__(self):
        sourceManager.__init__(self)
        self.template_fields['id'] = 'wtp id'
        self.template_fields['col_name'] = 'wtp name'
        self.template_fields['col_range'] = 'wtp range'
        self.template_fields['missing_vals'] = 'wtp missing value'
        self.data = None

        # Data table means which sql data table the wtp data comes from
        # User needs to provide it in the template. Empty string means
        # the user hasn't entered any. The program can quit
        self.data_table = []

    def _get_fieldnames_(self, desc):
        fieldnames = []
        for column in desc:
            fieldnames.append(column[0])
        return fieldnames


    def _read_data_from_source_(self):
        '''
        Follow the api for read data
        :return:
        '''
        data = []

        # TODO: allow multiple table
        con = pyodbc.connect("DSN=wtp_data")


        # To test the primary key. The primary key can be familyid and twin or just familyid.
        table_type = self.check_table_type(self.data_table[0], con)
        join_cmd = self.get_join_stmt(self.data_table, table_type)
        cursor = con.cursor()
        cursor.execute(join_cmd)
        desc = cursor.description
        fieldnames = self._get_fieldnames_(desc)

        import ipdb;ipdb.set_trace();
        # assert the data source has all the source fields defined in the template
        # so that no col_defs will map to nothing in the data source
        man_log.debug('expected fieldnames: %s' % self.col_defs)
        for col_name in self.col_defs:
            if col_name not in fieldnames:
                raise self.TemplateError(('expected column %s not '
                                          'found in source datafile, with fields: %s') % (
                                             col_name, list(fieldnames)))

        sql_data = cursor.fetchall()
        # load each row
        for rowid, datarow in enumerate(sql_data):
            man_log.info('loading row %s' % rowid)
            man_log.debug('parsing row %s : %s' % (rowid, datarow))
            row = utils.OrderedDict()
            for col in self.col_defs:
                try:
                    # Find the data position due to the fact that you can only access the data in datarow
                    # with index
                    col_name = col.col_name
                    index = fieldnames.index(col_name)

                    # prepare parser
                    col_parser_name = 'parse_' + str(col)
                    man_log.debug('parsing %s from %s using %s' % (col,
                                                                   datarow[index], col_parser_name))
                    col_parser = getattr(self, col_parser_name,
                                         self.default_parser)


                    # I parse everything into datarow
                    row[col] = col_parser(str(datarow[index]), col)
                except Exception as e:
                    man_log.debug('Exception while parsing %s: %s' % (col, e))
                    row[col] = self.NoDataError('%s' % e)
            data.append(row)
        con.close()
        return data

    def check_table_type(self, data_table, con):
        select_cmd = "select * from {0}".format(data_table)
        cursor = con.cursor()
        cursor.execute(select_cmd)
        desc = cursor.description
        fieldnames = self._get_fieldnames_(desc)
        if "twin" in fieldnames:
            return TableType.TwinTable
        return TableType.FamilyTable


    def get_join_stmt(self, data_tables, table_type):

        return "SELECT * FROM {0} AS T0 {1} ;".format(data_tables[0], self.join_stmt(data_tables, 1, table_type))

    def _compare_stmts(self, table_type, first_table_identifier, second_table_identifier):
        key_compare_strs = {
            TableType.TwinTable : "{0}.familyid = {1}.familyid AND {0}.twin = {1}.twin".format(first_table_identifier, second_table_identifier),
            TableType.FamilyTable : "{0}.familyid = {1}.familyid".format(first_table_identifier, second_table_identifier)
        }
        return key_compare_strs[table_type]

    def join_stmt(self, data_tables, index, table_type):

        if index == len(data_tables):
            return ""

        table = data_tables[index]
        last_table_identifier = "T{0}".format(index - 1)
        this_table_identifier = "T{0}".format(index)

        return "INNER JOIN ({0} AS {1} {2}) ON ({3})".format(table,
                                                             this_table_identifier,
                                                             self.join_stmt(data_tables, index+1, table_type),
                                                             self._compare_stmts(table_type, last_table_identifier,
                                                                                 this_table_identifier))

