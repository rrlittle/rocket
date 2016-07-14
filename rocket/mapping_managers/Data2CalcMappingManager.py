from MappingManagers import MappingManagers
from ..data_handlers wtpcalchandler
from ..Functions import default_func,data_sum,mean


class Data2CalcMM(MappingManagers):
	"""docstring for Data2CalcMM"""
	def __init__(self, source=sourceManager, sink = sinkManager):
		super(Data2CalcMM, self).__init__(source=sourceManager, 
											sink = sinkManager)
		
	def load_function(self):
		functions = {}
		functions['mean'] = mean
		functions['data_sum'] = data_sum


		return{};


		