from Functions.function_api import Function
from Functions.ursi_data_manager import get_ursi_data_manager
from Managers import sinkManager

def get_ursi_by_wbic(data_dict, wbic):
    for ursi, ursi_dict in data_dict.items():
        try:
            if ursi_dict["WBIC"] == wbic:
                return ursi
        except KeyError as e:
            raise sinkManager.DropRowException("WBIC or URSI key is not in the information file")


class FindGuidForWTPTwin (Function):

    def get_name(self):
        return "findGuidForWTPTwin"

    def _func_(self, data_list, args=None):

        #It will raise drop row exception
        #TODO: Add the body for the wtp twin. It should accept both familyid and twin
        return ""

class FindGuidForWTPFamily (Function):

    def get_name(self):
        return "findGuidForWTPFamily"

    def _func_(self, data_list, args=None):
        # TODO: Add the body for the looking up the guid for wtp family caregiver
        # It only accepts familyid.
        pass