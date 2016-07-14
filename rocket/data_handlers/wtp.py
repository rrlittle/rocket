from Managers import sourceManager, sinkManager
import utils
import re 

class wtp_source(sourceManager):
    ''' this is used to pull data and stuff from the wtp database 
        or yaml files defining the instruments and things 
    '''
    
    def __init__(self):
        sourceManager.__init__(self)


class wtp_sink(sinkManager):
    ''' this is used to write data and stuff to the wtp dtabase '''
    def __init__(self):
        sinkManager.__init__(self)
        self.template_fields['reversed'] = 'reversed?'

    def get_file_outpath(self):
        ''' this sets self.outpath, in the case of wtphandler that will be a tablename
            which tells the destination table
        '''
        if hasattr(self, 'outpath'): return self.outpath
        else:
            def validator(txt): 
                return len(re.findall(r'^[a-zA-Z][a-zA-Z_0-9]*$', txt)) == 1


            # really anything is valid
            self.outpath = utils.get_input(('enter the table you would like to save '
                'the data to\n this will overwrite the table. so be careful.'
                '\n if the table does not exist now, it will be overwritten'),
                validator=validator, errtxt ='{err} plaese try again')

            if self.outpath == None: 
                print(('you did not indicate where the data should go. '
                    'we can go no further'))
                utils.exit()

            return self.outpath 

    def write_outfile()