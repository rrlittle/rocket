from Managers import sourceManager, sinkManager
import utils
import re 

class wtp_source(sourceManager):
    ''' this is used to pull data and stuff from the wtp database 
        or yaml files defining the instruments and things 
    '''
    
    def __init__(self):
        sourceManager.__init__(self)
        self.con = utils.open_con(DSN='wtp_data')


class wtp_sink(sinkManager):
    ''' this is used to write data and stuff to the wtp dtabase '''
    def __init__(self):
        sinkManager.__init__(self)
        self.template_fields['reversed'] = 'reversed?'
        self.template_fields['pk'] = 'primary key?'

    def get_file_outpath(self):
        ''' this sets self.outpath, in the case of wtphandler that will be a tablename
            which tells the destination table
        '''
        if hasattr(self, 'outpath'): return self.outpath
        else:

            def validator(txt): 
                # ensure it's just a simple string that doesn't start with numbers
                return len(re.findall(r'^[a-zA-Z][a-zA-Z_0-9]*$', txt)) == 1

            self.outpath = utils.get_input(('enter the table you would like to save '
                'the data to\n this will overwrite the table. so be careful.'
                '\n if the table does not exist now, it will be overwritten'),
                validator=validator, errtxt ='{err} plaese try again')

            if self.outpath == None: 
                print(('you did not indicate where the data should go. '
                    'we can go no further'))
                utils.exit()

            return self.outpath 

    def write_outfile(self):
        ''' for the wtp we're actually writing to the database, not a csv. 
            so this is fairly different from the defualt.

            this does support making new tables because this forces the template to have 
            all the important info for defining the sink table if it doesn't already exist
        '''
        if self.outpath not in utils.db.get_tablenames(self.con):
            keys = [c for c in self.col_defs if c.pk]
            utils.db.create_table(self.con, self.outpath, self.col_defs, keys=None)

            
