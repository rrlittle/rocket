from data_handlers.wtp import WtpSource
from data_handlers.ndar import ndar_snk
from MappingManager import MappingManager
from Functions.calc_functions import Sum, Mean

class wtp2ndar (MappingManager):

    def __init__(self):
        super(wtp2ndar, self).__init__(source=WtpSource,
                                sink=ndar_snk)

    def load_functions(self):
        function_list = []
        function_list.append(Sum())
        function_list.append(Mean())
        return function_list

