from Functions.personal_info_functions import FindAge, FindGender, FindBirthdate
from Functions.ursi_data_manager import get_ursi_data_manager

# given wbic I can get ursi
def get_ursi_by_wbic(wbic):
    for ursi, ursi_dict in get_ursi_data_manager().get_ursi_data().items():
        try:
            if ursi_dict["WBIC"] == wbic:
                return ursi
        except KeyError as e:
            raise Exception("WBIC or URSI key is not in the information file")


class FindGenderByWBIC(FindGender):

    def get_name(self):
        return "findGenderByWBIC"

    def get_documentation(self):
        return "Same as findGender, except receive as a wbic"

    def convert_tag_to_ursi(self, tag_list):
        '''
            Convert the wbic tag to the ursi with the outside function.
        :param tag:
        :return:
        '''
        return get_ursi_by_wbic(tag_list[0])


class FindAgeByWBIC(FindAge):

    def get_name(self):
        return "findAgeByWBIC"

    def get_documentation(self):
        return "Same as findAge, except receive as a wbic"

    def convert_tag_to_ursi(self, tag_list):
        return get_ursi_by_wbic(tag_list[0])


class FindBirthdateByWBIC(FindBirthdate):

    def get_name(self):
        return "findBirthdateByWBIC"

    def get_documentation(self):
        return "Same as findBirthdate, except receive as a wbic"

    def convert_tag_to_ursi(self, tag_list):
        return get_ursi_by_wbic(tag_list[0])
