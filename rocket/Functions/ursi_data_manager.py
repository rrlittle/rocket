import os.path as path
from subprocess import PIPE, Popen, call
from ast import literal_eval
from os import stat
import utils
import logging
from __init__ import secretdir

class UrsiDataManager(object):
    def __init__(self, secret_dir_path, first_time_enter, PPIfilename, ppiscript = None, func_log = logging):
        self.first_time_enter = first_time_enter

        self.temp_file_path = path.join(secret_dir_path, PPIfilename)
        self.func_log = func_log
        self.data_list = []
        self.ppiscript = ppiscript

        # prepare the file. If it doesn't exist, prepare it. If it exists, no need for doing anything
        # Also check the empty of the file
        self.ensure_data_file_exist()

    # make the temp data file by using list_gender.bat
    def initialize_data_file(self):

        # log_time_interval = 5;
        # seconds_process = 0;

        # def log_time():
        #	global seconds_process
        #	seconds_process += 5
        #	print("It's still running, be patient, please. Running time: "
        #		"%s"%(seconds_process))

        # t = Timer(log_time_interval,log_time)
        # t.start()

        if path.exists(self.ppiscript) == False:
            self.func_log.critical(('get ppi script cannot be found. dir '
                               'contains %s') % utils.listdir(utils.dirname(self.ppiscript)))
            raise EnvironmentError('get ppi script cannot be found')

        print("Calling the get ppi script with ruby")
        process = Popen(self.ppiscript, stdout=PIPE)
        output = list(process.communicate())
        # t.cancel()
        # hard code the parse rule due to some bad thing
        # the data looks like this
        # (b"D, [2016-07-06T14:40:22.172340 #1676] DEBUG -- : Successfully logged into COINS.\r\n{{'M53799763':{'gender': 'F'}}\r\n{{'M53799718':{'gender': 'M'}}\r\n", None)
        string = output[0].decode()
        data = string.split('\r\n')[1:]

        print("Initializing the file")
        with open(self.temp_file_path, 'w') as tempfile:
            for subject in data:
                # tempfile.writelines()
                tempfile.write(subject + '\n')

    def get_ursi_data(self):
        data_dict = {}
        with open(self.temp_file_path, 'r') as tempfile:
            lines = tempfile.readlines()
            for row in lines:
                try:
                    subjectDict = literal_eval(row)
                    for ursi in subjectDict:
                        data_dict[ursi] = subjectDict[ursi]
                except SyntaxError as e:
                    self.func_log.debug('syntaxError in get_ursi_data: %s' % e)
                    pass
        return data_dict

    def ensure_data_file_exist(self):
        if path.exists(self.temp_file_path):
            # If the file is just an empty file, caused by a program crash last
            # I will still initialize it.
            if stat(self.temp_file_path).st_size == 0:
                self.initialize_data_file()
            else:
                # this will ask the user whether they want to update the personal information
                if (self.first_time_enter):
                    while True:
                        answer = input("We detect there is personal information file, do you want to update it? (yes/no)")
                        if answer == "yes":
                            print("Information updating")
                            self.initialize_data_file()
                            break
                        elif answer == "no":
                            print("Information will not update")
                            break
                        else:
                            print("Please enter yes or no")
                    self.first_time_enter = False

        else:
            self.initialize_data_file()

ursi_data_manager = None


def get_ursi_data_manager():
    global ursi_data_manager

    if ursi_data_manager is None:
        ursi_data_manager = UrsiDataManager(secretdir, True, 'coinsPersonal.tmp')

    return  ursi_data_manager


class Unittests():
    def __init__(self):
        self.findgender()
        self.findguid()

    def findgender(self):
        genderFinder = GenderByUrsi(data_list=['M53799718'])
        genderFinder.find_gender()

    def findguid(self):
        guidFinder = GuidByUrsi(data_list=['M53799718'])
        guidFinder.find()
