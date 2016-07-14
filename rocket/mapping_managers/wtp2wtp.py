from MappingManager import MappingManager
from data_handlers.wtp import wtp_source, wtp_sink

class wtp2wtp(MappingManager):
    ''' this handles mapping between two wtp data table formats
        i.e. data to calc or something
    '''

    def __init__(self):
        MappingManager.__init__(self, source = wtp_source, sink=wtp_sink)
        