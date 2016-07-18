from os import path
from os import stat
from subprocess import (PIPE,Popen,call)
from ast import literal_eval
<<<<<<< HEAD
from dateutil import relativedelta
from datetime import datetime

=======
from __init__ import sectretdir
>>>>>>> b2ed046c4b9fb68666e82d4b07148eb3e166051a

temp_data_path = 'ursi_data.tmp'

def findGender(ursi,args = None):

	print('finding the gender')
	ursi_data_manger = UrsiDataManager(temp_data_path)
	data_dict = ursi_data_manger.get_ursi_data()

	assert ursi !='', 'No ursi has been passed'
	gender = data_dict[ursi]["gender"]
	return gender

class UnitTestGender():

	def __init__(self):
		genderFinder = GenderByUrsi(data_list=  ['M53799718'])
		genderFinder.find_gender()

<<<<<<< HEAD
def findBirthdate(ursi,args = None):
	"""
		This function is called in the coins2ndar load_function().
=======
>>>>>>> b2ed046c4b9fb68666e82d4b07148eb3e166051a
		
		It will return a datetime object.
	"""
	DOB_dateformat = "%m/%d/%Y"
	data_dict = ursi_data_manger.get_ursi_data()
	assert ursi !='', 'No ursi has been passed'

	birth_date = data_dict[ursi]['birth_date']
	DOB_date = datetime.strptime(birth_date, DOB_dateformat);

<<<<<<< HEAD
	return DOB_date


def findGuid(ursi,args = None):
=======
>>>>>>> b2ed046c4b9fb68666e82d4b07148eb3e166051a
	data_dict =''
	ursi = ''
	GUID = ''

	ursi_data_manger = UrsiDataManager(temp_data_path)
	data_dict = ursi_data_manger.get_ursi_data()

	assert ursi !='', 'No ursi has been passed'

	GUID = data_dict[ursi]['GUID']

	return GUID

class UnitTestGuid():

	def __init__(self):
		guidFinder = GuidByUrsi(data_list=  ['M53799718'])
		guidFinder.find()


def findAge(olddate = None, recentdate = None):
	""" both argument will be the datetime object. The ndar way to calculate the
	age is the total 
	"""

	assert olddate != None and recentdate != None, "**** findAge goes wrong ***"

	age = relativedelta.relativedelta(olddate,recentdate)
	year = abs(age.years)
	month = abs(age.months)
	day = abs(age.days)
	if day > 15:
		month = month + 1

	total_months = year*12 + month
	return total_months

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

