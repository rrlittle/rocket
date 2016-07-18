from UrsiDataManager import UrsiDataManager
from Functions import Functions
import ipdb


def findGender(srcdat ,args = None):

	print('finding the gender')
	ursi_data_manger = UrsiDataManager('ursi_data.tmp')
	data_dict = ursi_data_manger.get_ursi_data()
	ursi = srcdat[0]

	assert ursi !='', 'No ursi has been passed'
	gender = data_dict[ursi]["gender"]
	return gender

class UnitTestGender():

	def __init__(self):
		genderFinder = GenderByUrsi(data_list=  ['M53799718'])
		genderFinder.find_gender()

def findBirthdate(srcdat,args = None):
	
	try:
		data_dict = ursi_data_manger.get_ursi_data()
		ursi_data_manger = UrsiDataManager('ursi_data.tmp')

		ursi = srcdat[0]
		assert ursi !='', 'No ursi has been passed'
		birth_date = data_dict[ursi]['birth_date']

	except AssertionError:
		pass
	
	return birth_date


def findGuid(srcdat,args = None):
	data_dict =''
	ursi = ''
	GUID = ''

	try:
		data_dict = self.ursi_data_manger.get_ursi_data()
	
		ursi = self.data_list[0]
		assert ursi !='', 'No ursi has been passed'

		GUID = data_dict[ursi]['GUID']
	except AssertionError:
		pass

	return GUID

class UnitTestGuid():

	def __init__(self):
		guidFinder = GuidByUrsi(data_list=  ['M53799718'])
		guidFinder.find()


class UrsiDataManager(object):

	def __init__(self,temp_file_path):
		self.temp_file_path = temp_file_path
		self.data_list = []
		self.BAT_PATH = 'R:\scripts\list_gender_birth_guid.bat'


		# prepare the file. If it doesn't exist, prepare it. If it exists, no need for doing anything
		# Also check the empty of the file		
		if path.exists(self.temp_file_path):
			if stat(self.temp_file_path).st_size == 0:
				self.initialize_data_file()

		else:
			self.initialize_data_file()


	# make the temp data file by using list_gender.bat
	def initialize_data_file(self):
		if path.exists(self.BAT_PATH) == False:
			raise Exception('Bat cannot be found')

		print("Calling the bat")
		process = Popen(self.BAT_PATH, stdout = PIPE)
		output = list(process.communicate())
	
		# hard code the parse rule due to some bad thing
		# the data looks like this
		# (b"D, [2016-07-06T14:40:22.172340 #1676] DEBUG -- : Successfully logged into COINS.\r\n{{'M53799763':{'gender': 'F'}}\r\n{{'M53799718':{'gender': 'M'}}\r\n", None)
		string = output[0].decode()
		data = string.split('\r\n')[1:]

		print ("Initializing the file")
		with open(self.temp_file_path,'w') as tempfile:
			for subject in data:
				#tempfile.writelines()
				tempfile.write(subject+'\n')


	def get_ursi_data(self):
		data_dict = {}
		with open(self.temp_file_path,'r') as tempfile:
			lines = tempfile.readlines()
			for row in lines:
				try:
					subjectDict = literal_eval(row)
					for ursi in subjectDict:
						data_dict[ursi] = subjectDict[ursi]
				except SyntaxError:
					pass
		return data_dict
