import pyodbc
from collections import OrderedDict

def _get_fieldnames_(desc):
    fieldnames = []
    for column in desc:
        fieldnames.append(column[0])
    return fieldnames
data=[]
tablename = "user_3_disc_091509"
con = pyodbc.connect("DSN=wtp_data")
select_cmd = "select * from {0}".format(tablename)
cursor = con.cursor()
cursor.execute(select_cmd)
desc = cursor.description
fieldnames = _get_fieldnames_(desc)

cols = ["pgasymp3", "pagsymp3", "pocsymp3"]

# assert the file has all the expected fields
#man_log.debug('expected fieldnames: %s' % self.col_defs)
for col_name in cols:
    if col_name not in fieldnames:
        raise Exception(('expected column %s not '
                                  'found in source datafile, with fields: %s') % (
                                     col_name, list(fieldnames)))

sql_data = cursor.fetchall()
# load each row
for rowid, datarow in enumerate(sql_data):
    # man_log.info('loading row %s' % rowid)
    # man_log.debug('parsing row %s : %s' % (rowid, datarow))
    row = OrderedDict()
    for col in cols:
        #try:
        col_parser_name = 'parse_' + str(col)
        #man_log.debug('parsing %s from %s using %s' % (col,
         #                                              datarow[col], col_parser_name))
        #col_parser = getattr(self, col_parser_name,
         #                    self.default_parser)
        col_name = col
        index = fieldnames.index(col_name)

        row[col] = str(datarow[index])
        #except Exception as e:
         #   print('Exception while parsing %s: %s' % (col, e))
            #row[col] = self.NoDataError('%s' % e)
            #pass
    data.append(row)

print(data)