from MappingManager import MappingManager
from data_handlers import coins, ndar
import Functions as func

class coins2ndar(MappingManager):
    ''' this manager is to define the mappping between coins and ndar type files.
    '''

    def __init__(self):
        ''' this initializes a mapping manager with coins as source and ndar as sink
        '''
        MappingManager.__init__(self, 
            source = coins.coins_src, 
            sink=ndar.ndar_snk)

    def load_functions(self):
        functions = {}
        functions['mean'] = {'ref':func.mean}
        functions['data_sum']   = {'ref':func.data_sum}
        functions['findGender'] = {'ref':func.ursi_functions.findGender}
        functions['findGuid'] = {'ref':func.ursi_functions.findGuid}
        return functions        
