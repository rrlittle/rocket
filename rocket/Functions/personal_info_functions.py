from Functions.function_api import Function
from Functions.ursi_data_manager import get_ursi_data_manager
from dateutil import relativedelta
from datetime import datetime


class FindAge (Function):

    '''
        Base class for find age
    '''

    def get_documentation(self):
        return "Find the participants's Age based on the given ursi, and assessment date. " \
               "Put two coins id into the mapping id.Like 1,4"

    def get_name(self):
        return "findAge"
    
    def findBirthdate(self, ursi, args=None):
        """
            This function is called in the coins2ndar load_function().
            It will return a datetime object.
        """
        DOB_dateformat = "%m/%d/%Y"
        # ursi_data_manager = UrsiDataManager(temp_data_path,first_time_enter)
        ursi_data_manager = get_ursi_data_manager()
        data_dict = ursi_data_manager.get_ursi_data()
        assert ursi != '', 'No ursi has been passed'

        birth_date = data_dict[ursi]['birth_date']
        DOB_date = datetime.strptime(birth_date, DOB_dateformat)

        return DOB_date

    def convert_tag_to_ursi(self, tag_data):
        '''
            Overridable. making the data with the data
        :param tag:
        :return:
        '''
        return tag_data[0]


    def _func_(self, data_list, args=None):

        ursi = self.convert_tag_to_ursi(data_list)
        olddate = self.findBirthdate(ursi)
        recentdate = data_list[-1]
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


class FindBirthdate(Function):

    def get_name(self):
        return "findBirthdate"

    def find_birthdate(self, ursi, args=None):
        """
            This function is called in the coins2ndar load_function().
            It will return a datetime object.
        """
        DOB_dateformat = "%m/%d/%Y"

        ursi_data_manager = get_ursi_data_manager()
        data_dict = ursi_data_manager.get_ursi_data()
        assert ursi != '', 'No ursi has been passed'

        birth_date = data_dict[ursi]['birth_date']
        DOB_date = datetime.strptime(birth_date, DOB_dateformat)

        return DOB_date

    def convert_tag_to_ursi(self, tag_data):
        '''
            Overridable.
        :param tag: the other kind of tag.
        :return:
        '''
        return tag_data[0]

    def _func_(self, data_list, args=None):
        return self.find_birthdate(self.convert_tag_to_ursi(data_list))


class FindGender(Function):
    def __init__(self ,*args, **kwargs):
        super(FindGender, self).__init__(*args, **kwargs)

    def get_documentation(self):
        return "Find the participant's gender based on ursi"

    def get_name(self):
        return "findGender"

    def convert_tag_to_ursi(self, tag_data):
        '''
            Overridable.
        :param tag_data: Be careful that tag_data is a list. Just get the data that you need
        :return:
        '''
        return tag_data[0]

    def _func_(self, data_list, args=None):
        print('finding the gender')
        ursi = self.convert_tag_to_ursi(data_list)
        assert ursi != '', 'No ursi has been passed'

        ursi_data_manager = get_ursi_data_manager()
        data_dict = ursi_data_manager.get_ursi_data()
        gender = data_dict[ursi]["gender"]
        return gender