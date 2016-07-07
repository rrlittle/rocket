from  UrsiFunctions import UrsiFunctions
from UrsiDataManager import UrsiDataManager

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
		gender = data_dict[ursi][self.GENDER_MAP]
		return gender



class UnitTest():

	def __init__(self):
		genderFinder = GenderByUrsi(data_list=  ['M53799718'])
		genderFinder.find_gender()


genderFinder = GenderByUrsi(data_list=  ['M53799718'])
genderFinder.find()