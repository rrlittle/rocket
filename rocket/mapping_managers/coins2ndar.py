from MappingManager import MappingManager
from data_handlers import coins, ndar
import Functions as func
from Functions import ursi_functions
from loggers import map_log
from __init__ import templatedir,secretdir

class coins2ndar(MappingManager):
	''' this manager is to define the mappping between coins and ndar type files.
	'''



	def __init__(self):
		''' this initializes a mapping manager with coins as source and ndar as sink
		'''
		MappingManager.__init__(self, 
			source = coins.coins_src, 
			sink=ndar.ndar_snk)
		# print('functions', self.globalfuncs)
		ursi_data_manager = ursi_functions.UrsiDataManager(secretdir)
		if self.want_update_ursi_data:
			ursi_data_manager.initialize_data_file();

	
	def load_functions(self):
		functions = {}

		def findAge(ursi, ass_date, args=None):

			''' finds the age from the ursi and the assment date
				requires the ursi first and ass_date second'''
			map_log.critical("Ursi: %s, ass_date: %s" %(ursi, ass_date))

			bd = ursi_functions.findBirthdate(ursi)


			return ursi_functions.findAge(olddate=bd, recentdate=ass_date)


		functions['mean'] = {'ref':func.mean}
		functions['sum']   = {'ref':func.sum}
		functions['findGender'] = {'ref':ursi_functions.findGender}
		functions['findGuid'] = {'ref':ursi_functions.findGuid}
		functions['findAge'] = {'ref':findAge}
		return functions


	def want_update_ursi_data(self):
		yes = 'y'
		no = 'n'
		while True:
			user_in = input("The personal data from Coins has already been downloaded,"
				"do you want to redownload it? (y/n) ")
			if user_in[0].lower == yes:
				return True
			elif user_in[0].lower == no:
				return False


