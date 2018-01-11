from dateutil import relativedelta
from datetime import datetime
from __init__ import secretdir, waisman_user, scriptdir
import utils
from loggers import func_log
from Functions.function_api import Function, DropRowFunction
from Functions.ursi_data_manager import get_ursi_data_manager
from Managers import ssManager
# where to store secret files i.e. coins secret key and PPI file
temp_data_path = secretdir

# filename to store PPI file
PPIfilename = 'coinsPersonal.tmp'

get_ppi_script_ext = None
if utils.systemName in ('Linux', 'Darwin'):  # use the
    get_ppi_script_ext = '.sh'
elif utils.systemName in ('Windows'):  #
    get_ppi_script_ext = '.bat'
else:
    func_log.critical('This platform is not supported!')
    utils.exit()

get_ppi_script_filename = 'list_gender_birth_guid' + get_ppi_script_ext
get_ppi_script_path = utils.join(scriptdir, get_ppi_script_filename)
func_log.info('ppi script is %s' % get_ppi_script_path)
first_time_enter = True

dateformat_candidates =[
    "%m/%d/%Y %H:%M",
    "%m-%d-%Y %I:%M:%S %p",
    "%m/%d/%Y"
]

def parse_assessment_date(assessment_date):
    for dateformat in dateformat_candidates:
        try:
            assessment_date = utils.datetime.strptime(assessment_date,
                                                      dateformat)
            return assessment_date
        except Exception as e:
            pass

    raise ValueError("The assessment_date in data file is not matched in any acceptable date format in rocket")


def findBirthdate(ursi, args=None):
    """
        This function is called in the coins2ndar load_function().
        It will return a datetime object.
    """
    DOB_dateformat = "%m/%d/%Y"
    #ursi_data_manager = UrsiDataManager(temp_data_path,first_time_enter)
    ursi_data_manager = get_ursi_data_manager()
    data_dict = ursi_data_manager.get_ursi_data()
    assert ursi != '', 'No ursi has been passed'

    birth_date = data_dict[ursi]['birth_date']
    DOB_date = datetime.strptime(birth_date, DOB_dateformat)

    return DOB_date

def findBirthdateByWBIC(wbic, args= None):
    DOB_dateformat = "%m/%d/%Y"
    #ursi_data_manager = UrsiDataManager(temp_data_path, first_time_enter)
    ursi_data_manager = get_ursi_data_manager()
    data_dict = ursi_data_manager.get_ursi_data()
    ursi = get_ursi_by_wbic(data_dict=data_dict, wbic=wbic)
    assert ursi != '', 'No ursi has been passed'

    birth_date = data_dict[ursi]['birth_date']
    DOB_date = datetime.strptime(birth_date, DOB_dateformat)
    return DOB_date


# Help Function
def get_ursi_by_wbic(data_dict, wbic):
    for ursi, ursi_dict in data_dict.items():
        try:
            if ursi_dict["WBIC"] == wbic:
                return ursi
        except KeyError as e:
            raise Exception("WBIC or URSI key is not in the information file")

class FindUrsiByWBIC(DropRowFunction):

    def get_documentation(self):
        return "Find the participants' ursi given a wbic"

    def get_name(self):
        return "findUrsiByWbic"

    def _func_(self, data_list, args=None):
        # given wbic I can get ursi

        # The first element is considered as ursi.
        wbic = data_list[0]

        for ursi, ursi_dict in get_ursi_data_manager().get_ursi_data().items():
            try:
                if ursi_dict["WBIC"] == wbic:
                    return ursi
            except KeyError as e:
                raise Exception("WBIC or URSI key is not in the information file")

        # how to deal with data not found? Raise exception that will drop the row or return null?
        return None

class FindGender(Function):
    def __init__(self,*args,**kwargs):
        super(FindGender, self).__init__(*args, **kwargs)

    def get_documentation(self):
        return "Find the participant's gender based on ursi"

    def get_name(self):
        return "findGender"

    def _func_(self, data_list, args=None):
        print('finding the gender')
        ursi = data_list[0]
        assert ursi != '', 'No ursi has been passed'

        #ursi_data_manager = UrsiDataManager(temp_data_path, first_time_enter)
        ursi_data_manager = get_ursi_data_manager()
        data_dict = ursi_data_manager.get_ursi_data()
        gender = data_dict[ursi]["gender"]
        return gender


class FindGenderByWBIC(Function):
    def get_name(self):
        return "findGenderByWBIC"

    def get_documentation(self):
        return "Same as findGender, except receive as a wbic"

    def _func_(self, data_list, args=None):
        print('finding the gender')
        wcib = data_list[0]
        #ursi_data_manager = UrsiDataManager(temp_data_path, first_time_enter)
        ursi_data_manager = get_ursi_data_manager()
        data_dict = ursi_data_manager.get_ursi_data()

        # convert wcib to ursi, use that as a key
        ursi = get_ursi_by_wbic(data_dict, wcib)
        assert ursi != '', 'No ursi has been passed'


        gender = data_dict[ursi]["gender"]
        return gender


class FindBirthdateByWBIC(Function):
    def get_name(self):
        return "findBirthdateByWBIC"

    def get_documentation(self):
        return "Same as FindBirthdate, but it accepts a wbic as input"

    def _func_(self, data_list, args=None):

        return findBirthdateByWBIC(data_list[0])


class FindBirthdate(Function):
    def __init__(self,*args, **kwargs):
        super(FindBirthdate, self).__init__(*args,**kwargs)

    def get_name(self):
        return "findBirthdate"

    def _func_(self, data_list, args=None):
        return findBirthdate(data_list[0])

class FindGuid(DropRowFunction):
    def get_documentation(self):
        return "Find the participants's GUID based on the given ursi"

    def get_name(self):
        return "findGuid"

    def _func_(self, data_list, args=None):
        data_dict = ''
        GUID = ''
        ursi = data_list[0]

        #ursi_data_manager = UrsiDataManager(temp_data_path, first_time_enter)
        ursi_data_manager = get_ursi_data_manager()
        data_dict = ursi_data_manager.get_ursi_data()

        assert ursi != '', 'No ursi has been passed'
        GUID = data_dict[ursi]['GUID']
        if GUID == "NONE":
            raise Exception(('No guid found '
                                 'matching ursi %s') % ursi)

        return GUID


class FindAge(Function):
    def get_documentation(self):
        return "Find the participants's Age based on the given ursi, and assessment date. " \
               "Put two coins id into the mapping id.Like 1,4"

    def get_name(self):
        return "findAge"

    def _func_(self, data_list, args=None):
        """ both argument will be the datetime object. The ndar way to calculate the
            age is the total
            """

        ursi = data_list[0]
        olddate = findBirthdate(ursi)
        #recentdate = parse_assessment_date(data_list[1])
        recentdate = data_list[1];
        assert olddate != None and recentdate != None, "**** findAge goes wrong ***"
        # import ipdb; ipdb.set_trace()

        age = relativedelta.relativedelta(olddate, recentdate)
        year = abs(age.years)
        month = abs(age.months)
        day = abs(age.days)
        if day > 15:
            month = month + 1

        total_months = year * 12 + month
        return total_months


class FindAgeByWBIC(Function):
    def get_name(self):
        return "findAgeByWBIC"

    def get_documentation(self):
        return "Same as findAge, except it receives a wbic"

    def _func_(self, data_list, args=None):
        wbic = data_list[0]

        olddate = findBirthdateByWBIC(wbic)
        recentdate = data_list[1]

        assert olddate != None and recentdate != None, "**** findAge goes wrong ***"
       # import ipdb; ipdb.set_trace()

        age = relativedelta.relativedelta(olddate, recentdate)
        year = abs(age.years)
        month = abs(age.months)
        day = abs(age.days)
        if day > 15:
            month = month + 1

        total_months = year * 12 + month
        return total_months


class FindGuidByWBIC (DropRowFunction):
    """"""
    def get_name(self):
        return "FindGuidByWbic"

    def _func_(self, data_list, args=None):

        wbic = data_list[0]
        assert wbic != "", "The wbic passed in has nothing "

        # import ipdb;ipdb.set_trace()

        #ursi_data_manager = UrsiDataManager(temp_data_path, first_time_enter)
        ursi_data_manager = get_ursi_data_manager()
        data_dict = ursi_data_manager.get_ursi_data()
        for ursi, ursi_dict in data_dict.items():
            try:
                if ursi_dict["WBIC"] == wbic:

                    guid = ursi_dict["GUID"]
                    # Check whether the guid is None
                    if guid == "NONE":
                        raise KeyError()
                    else:
                        return guid

            except KeyError as e:
                raise Exception("WBIC or GUID key is not in the information file")

        raise Exception("The WBIC provided can't be found")

'''
class UrsiDataManager(object):
    def __init__(self, secret_dir_path, first_time_enter):
        self.first_time_enter = first_time_enter

        self.temp_file_path = path.join(secret_dir_path, PPIfilename)

        self.data_list = []
        self.ppiscript = get_ppi_script_path

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
            func_log.critical(('get ppi script cannot be found. dir '
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
                    func_log.debug('syntaxError in get_ursi_data: %s' % e)
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
                    global first_time_enter
                    first_time_enter = False

        else:
            self.initialize_data_file()'''
