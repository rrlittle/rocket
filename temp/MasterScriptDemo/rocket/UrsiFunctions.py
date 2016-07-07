from UrsiDataManager import UrsiDataManager
from Functions import Functions

class UrsiFunctions(Functions):
	
	#global URSI_DATA_LINK = 'ursi_data.tmp'

	def __init__(self,  sink_missing_val = '', 
		source_missing_val = '',
		data_list = [''],
		):
		super(UrsiFunctions,self).__init__(sink_missing_val, 
		source_missing_val,
		data_list)
		URSI_DATA_LINK = 'ursi_data.tmp'
		self.ursi_data_manger = UrsiDataManager(URSI_DATA_LINK)


	def find(self):
		print("GENERIC ANSWER")

class GenderByUrsi(UrsiFunctions):

#	global 

#	def __init__(self):
#		self.data_list = ['M53799718']

	def __init__(self,  sink_missing_val = '', 
		source_missing_val = '',
		data_list = ['']
		):
		super(GenderByUrsi,self).__init__(sink_missing_val, 
		source_missing_val,data_list)
		self.MAP = 'gender'


	def find(self):

		print('finding the gender')
		#self.ursi_data_manger = UrsiDataManager('ursi_data.tmp')
		data_dict = self.ursi_data_manger.get_ursi_data()
		ursi = self.data_list[0]
		assert ursi !='', 'No ursi has been passed'
		gender = data_dict[ursi][self.MAP]
		return gender



class UnitTestGender():

	def __init__(self):
		genderFinder = GenderByUrsi(data_list=  ['M53799718'])
		genderFinder.find_gender()
		
class BirthdateByUrsi(UrsiFunctions):

	def __init__(self,  sink_missing_val = '', 
		source_missing_val = '',
		data_list = ['']
		):
		super(BirthdateByUrsi,self).__init__(sink_missing_val, 
		source_missing_val,data_list)
		self.MAP = 'birth_date'

	def find(self):
		data_dict = self.ursi_data_manger.get_ursi_data()
		ursi = self.data_list[0]
		assert ursi !='', 'No ursi has been passed'
		birth_date = data_dict[ursi][self.MAP]
		print (birth_date)
		return birth_date

class UnitTestBirthdate():

	def __init__(self):
		birthdateFinder = BirthdateByUrsi(data_list=  ['M53799718'])
		birthdateFinder.find()

class GuidByUrsi(UrsiFunctions):

	def __init__(self,  sink_missing_val = '', 
		source_missing_val = '',
		data_list = ['']
		):
		super(GuidByUrsi,self).__init__(sink_missing_val, 
		source_missing_val,data_list)
		self.MAP = 'GUID'

	def find(self):
		data_dict = self.ursi_data_manger.get_ursi_data()
		ursi = self.data_list[0]
		assert ursi !='', 'No ursi has been passed'
		GUID = data_dict[ursi][self.MAP]
		return GUID

class UnitTestGuid():

	def __init__(self):
		guidFinder = GuidByUrsi(data_list=  ['M53799718'])
		guidFinder.find()
