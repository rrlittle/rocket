from UrsiFunctions import UrsiFunctions

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

class UnitTest():

	def __init__(self):
		birthdateFinder = BirthdateByUrsi(data_list=  ['M53799718'])
		birthdateFinder.find()

birthdateFinder = BirthdateByUrsi(data_list=  ['M53799718'])
birthdateFinder.find()
