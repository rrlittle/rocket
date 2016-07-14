from MappingManager import MappingManager
from data_handlers import coins, ndar

class coins2ndar(MappingManager):
    ''' this manager is to define the mappping between coins and ndar type files.
    '''

    def __init__(self):
        ''' this initializes a mapping manager with coins as source and ndar as sink
        '''
        MappingManager.__init__(self, 
            source = coins.coins_src, 
            sink=ndar.ndar_snk)
