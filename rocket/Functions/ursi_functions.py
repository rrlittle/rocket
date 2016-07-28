from os import path
from os import stat
from subprocess import PIPE,Popen,call
from ast import literal_eval
from dateutil import relativedelta
from datetime import datetime
from __init__ import secretdir, waisman_user, scriptdir
from Managers import sinkManager
from threading  import Timer
import utils
from loggers import func_log
# where to store secret files i.e. coins secret key and PPI file
temp_data_path = secretdir

# filename to store PPI file
PPIfilename = 'coinsPersonal.tmp'

get_ppi_script_ext = None
if utils.systemName in ('Linux', 'Darwin'): # use the 
	get_ppi_script_ext = '.sh'
elif utils.systemName in ('Windows'): # 
	get_ppi_script_ext = '.bat'
else: 
	func_log.critical('This platform is not supported!')
	utils.exit()

get_ppi_script_filename = 'list_gender_birth_guid' + get_ppi_script_ext
get_ppi_script_path = utils.join(scriptdir, get_ppi_script_filename)
func_log.info('ppi script is %s'%get_ppi_script_path)

def findGender(ursi,args = None):

	print('finding the gender')
	ursi_data_manager = UrsiDataManager(temp_data_path)
	data_dict = ursi_data_manager.get_ursi_data()

	assert ursi !='', 'No ursi has been passed'
	gender = data_dict[ursi]["gender"]
	return gender

def findBirthdate(ursi,args = None):
	"""
		This function is called in the coins2ndar load_function().
		It will return a datetime object.
	"""
	DOB_dateformat = "%m/%d/%Y"
	ursi_data_manager = UrsiDataManager(temp_data_path)
	data_dict = ursi_data_manager.get_ursi_data()
	assert ursi !='', 'No ursi has been passed'

	birth_date = data_dict[ursi]['birth_date']
	DOB_date = datetime.strptime(birth_date, DOB_dateformat);


	return DOB_date

def findGuid(ursi,args = None):
	data_dict =''
	GUID = ''
	ursi_data_manager = UrsiDataManager(temp_data_path)
	data_dict = ursi_data_manager.get_ursi_data()
	
	try:
		assert ursi !='', 'No ursi has been passed'
		GUID = data_dict[ursi]['GUID']
		

		if GUID == "NONE":
			raise sinkManager.DropRowException(('No guid found '
				'matching ursi %s')%ursi)

	except Exception as e:	
		raise sinkManager.DropRowException(e)

	return GUID

def findAge(olddate = None, recentdate = None):
	""" both argument will be the datetime object. The ndar way to calculate the
	age is the total 
	"""

	assert olddate != None and recentdate != None, "**** findAge goes wrong ***"

	#import ipdb; ipdb.set_trace()

	age = relativedelta.relativedelta(olddate,recentdate)
	year = abs(age.years)
	month = abs(age.months)
	day = abs(age.days)
	if day > 15:
		month = month + 1

	total_months = year*12 + month
	return total_months

class UrsiDataManager(object):

	def __init__(self,secret_dir_path):
		
		

		self.temp_file_path = path.join(secret_dir_path,PPIfilename)
		self.data_list = []
		self.ppiscript = get_ppi_script_path
		
		# prepare the file. If it doesn't exist, prepare it. If it exists, no need for doing anything
		# Also check the empty of the file		
		self.ensure_data_file_exist()

	# make the temp data file by using list_gender.bat
	def initialize_data_file(self):

		#log_time_interval = 5;
		#seconds_process = 0;
		
		#def log_time():
		#	global seconds_process
		#	seconds_process += 5
		#	print("It's still running, be patient, please. Running time: "
		#		"%s"%(seconds_process))
			
		#t = Timer(log_time_interval,log_time)
		#t.start()

		if path.exists(self.ppiscript) == False:
			func_log.critical(('get ppi script cannot be found. dir '
				'contains %s')%utils.listdir(utils.dirname(self.ppiscript)))
			raise EnvironmentError('get ppi script cannot be found')

		print("Calling the get ppi script with ruby")
		process = Popen(self.ppiscript, stdout = PIPE)
		output = list(process.communicate())
		#t.cancel()
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
				except SyntaxError as e:
					func_log.debug('syntaxError in get_ursi_data: %s'%e)
					pass
		return data_dict

	def ensure_data_file_exist(self):
		if path.exists(self.temp_file_path):
			if stat(self.temp_file_path).st_size == 0:
				self.initialize_data_file()

		else:
			self.initialize_data_file()


class Unittests():

	def __init__(self):
		self.findgender()
		self.findguid()
	def findgender(self):
		genderFinder = GenderByUrsi(data_list=  ['M53799718'])
		genderFinder.find_gender()
	def findguid(self):
		guidFinder = GuidByUrsi(data_list=  ['M53799718'])
		guidFinder.find()

