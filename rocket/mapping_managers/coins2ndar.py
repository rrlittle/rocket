from MappingManager import MappingManager
from data_handlers import coins, ndar
import Functions as func
from Functions import ursi_functions

class coins2ndar(MappingManager):
	''' this manager is to define the mappping between coins and ndar type files.
	'''

	def __init__(self):
		''' this initializes a mapping manager with coins as source and ndar as sink
		'''
		MappingManager.__init__(self, 
			source = coins.coins_src, 
			sink=ndar.ndar_snk)
		print('functions', self.globalfuncs)
	def load_functions(self):
		functions = {}

		def findAge(ursi, ass_date,args=None):
			''' finds the age from the ursi and the assment date
				requires the ursi first and ass_date second'''
			bd = ursi_functions.findBirthdate(ursi)
			return ursi_functions.findAge(olddate=bd, recentdate=ass_date)


		functions['mean'] = {'ref':func.mean}
		functions['sum']   = {'ref':func.sum}
		functions['findGender'] = {'ref':ursi_functions.findGender}
		functions['findGuid'] = {'ref':ursi_functions.findGuid}
		functions['findAge'] = {'ref':findAge}
		return functions
