from UrsiFunctions import UrsiFunctions

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

class UnitTest():

	def __init__(self):
		guidFinder = GuidByUrsi(data_list=  ['M53799718'])
		guidFinder.find()

guidFinder = GuidByUrsi(data_list=  ['M53799718'])
guidFinder.find()
