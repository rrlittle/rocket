from Functions.function_api import Function, DropRowFunction, DropRowException
from Functions.ursi_data_manager import get_ursi_data_manager
from Functions.personal_info_functions import FindBirthdate, FindGender, FindAge
from Functions.wbic_functions import FindBirthdateByWBIC, FindAgeByWBIC, FindGenderByWBIC
from Managers import sinkManager

'''
    The whole idea of the inheritance chain is that we first convert wtp id to wbic, and then turn wbic to ursi for
    further search. For visualization, WTPID -> WBIC -> URSI.
    The process of "WBIC -> URSI" has been implemented in the wbic function, thus I just need to decorate the function
    that implements "WTPID -> WBIC" in the front of the conversion function that converts from WBIC to URSI, that is
    the old convert_tag_to_ursi. The decorator function is called convert_wtp_to_wbic

'''

def convert_wtpfamily_to_wbic_decorator(conv_func):
    '''
        Decorator function for convert wtpfamilyid to wbic
    :param conv_func:
    :return:
    '''
    def wrapper(self, *args, **kwargs):
        familyid = args[0][0]
        wbic = generate_wbic_with_familyid_twin(familyid)
        return conv_func(self,[wbic])
    return wrapper

def convert_wtptwin_to_wbic_decorator(conv_func):
    '''

    :param conv_func:
    :return:
    '''
    def wrapper(self, *args, **kwargs):
        familyid = args[0][0]
        twin_num = args[0][1]
        wbic = generate_wbic_with_familyid_twin(familyid, twin_num)
        return conv_func(self,[wbic])
    return wrapper


def generate_wbic_with_familyid_twin(familyid, twin_num_string=None):
    '''

    :param familyid:
    :param twin_num_string:
    :return:
    '''
    if twin_num_string is not None:
        return familyid[3:] + twin_num_string
    return familyid[3:] + "3"

def get_ursi_by_wbic(data_dict, wbic):
    for ursi, ursi_dict in data_dict.items():
        try:
            if ursi_dict["WBIC"] == wbic:
                return ursi
        except KeyError as e:
            raise DropRowException("WBIC or URSI key is not in the information file")

def lookup_guid_with_wbic(wbic):

    ursi = get_ursi_by_wbic(get_ursi_data_manager().get_ursi_data(), wbic)
    guid = get_ursi_data_manager().get_ursi_data()[ursi]["GUID"]

    if guid == "NONE":
        raise Exception("GUID can't be found for this wtp family")

    return guid


class FindGuidForWTPTwin (DropRowFunction):

    def get_name(self):
        return "findGuidForWTPTwin"

    def get_documentation(self):
        return "Given familyid and twin, the function will return the guid associated with this family member"


    def _func_(self, data_list, args=None):

        # It will raise drop row exception
        # TODO: Add the body for the wtp twin. It should accept both familyid and twin
        familyid = data_list[0]
        twin_num = data_list[1]

        # validate input.
        assert "WTP" in familyid, "Familyid doesn't in the right format"
        assert twin_num == "1" or twin_num == "2", "Twin number is not 1 or 2"

        wbic = generate_wbic_with_familyid_twin(familyid, twin_num)

        return lookup_guid_with_wbic(wbic)


class FindGuidForWTPFamily (DropRowFunction):

    def get_name(self):
        return "findGuidForWTPFamily"

    def get_documentation(self):
        return "Given familyid, the function will return the guid associated with this family member"

    def _func_(self, data_list, args=None):
        # TODO: Add the body for the looking up the guid for wtp family caregiver
        # It only accepts familyid.

        familyid = data_list[0]

        assert "WTP" in familyid, "Familyid is not in the right format"
        wbic = generate_wbic_with_familyid_twin(familyid)

        return lookup_guid_with_wbic(wbic)


class FindAgeForWTPFamily(FindAgeByWBIC):
    def get_documentation(self):
        return ""

    def get_name(self):
        return "findAgeForWTPFamily"

    @convert_wtpfamily_to_wbic_decorator
    def convert_tag_to_ursi(self, tag_data):
        return super(FindAgeForWTPFamily, self).convert_tag_to_ursi(tag_data)


class FindAgeForWTPTwin(FindAgeByWBIC):
    def get_documentation(self):
        return ""

    def get_name(self):
        return "findAgeForWTPTwin"

    @convert_wtptwin_to_wbic_decorator
    def convert_tag_to_ursi(self, tag_data):
        return super(FindAgeForWTPTwin, self).convert_tag_to_ursi(tag_data)


class FindBirthdateForWTPFamily(FindBirthdateByWBIC):
    def get_name(self):
        return "findBirthdateForWTPFamily"
    
    def get_documentation(self):
        return ""
    
    @convert_wtpfamily_to_wbic_decorator
    def convert_tag_to_ursi(self, tag_list):
        return super(FindBirthdateForWTPFamily, self).convert_tag_to_ursi(tag_list)


class FindBirthdateForWTPTwin(FindBirthdateByWBIC):
    def get_name(self):
        return "findBirthdateForWTPTwin"

    def get_documentation(self):
        return ""
    
    @convert_wtptwin_to_wbic_decorator
    def convert_tag_to_ursi(self, tag_list):
        return super(FindBirthdateForWTPTwin, self).convert_tag_to_ursi(tag_list)


class FindGenderForWTPTwin(FindGenderByWBIC):
    def get_documentation(self):
        return ""
    
    def get_name(self):
        return "findGenderForWTPTwin"
    
    @convert_wtptwin_to_wbic_decorator
    def convert_tag_to_ursi(self, tag_list):
        return super(FindGenderForWTPTwin, self).convert_tag_to_ursi(tag_list)


class FindGenderForWTPFamily(FindGenderByWBIC):
    def get_name(self):
        return "findGenderForWTPFamily"
    
    def get_documentation(self):
        return ""
    
    @convert_wtpfamily_to_wbic_decorator
    def convert_tag_to_ursi(self, tag_list):
        return super(FindGenderForWTPFamily, self).convert_tag_to_ursi(tag_list)
