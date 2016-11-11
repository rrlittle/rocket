from Functions.calc_functions import data_sum, mean
from MappingManager import MappingManager
from data_handlers.wtp import wtp_source, wtp_sink


class wtp2wtp(MappingManager):
    '''this handles mapping between two wtp data table formatsi.e.
     data to calc or something'''
    def __init__(self):
        MappingManager.__init__(self, source = wtp_source, sink=wtp_sink)
        
    def load_function(self):
        functions = {}
        functions['mean'] = mean
        functions['data_sum'] = data_sum
        return functions