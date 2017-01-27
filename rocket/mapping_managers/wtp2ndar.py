from data_handlers.wtp import WtpSource
from data_handlers.ndar import ndar_snk
from MappingManager import MappingManager
from Functions.calc_functions import Sum, Mean
from template_kit.template_structure import TemplateStructure
from template_kit.TemplateComponents import DataTableComponent
from Functions.wtpdata_functions import FindGuidForWTPFamily, FindGuidForWTPTwin, FindBirthdateForWTPTwin,FindAgeForWTPTwin\
    , FindGenderForWTPTwin, FindBirthdateForWTPFamily, FindGenderForWTPFamily, FindAgeForWTPFamily


class wtp2ndar (MappingManager):

    def __init__(self):
        super(wtp2ndar, self).__init__(source=WtpSource,
                                        sink=ndar_snk)

    def load_functions(self):
        function_list = []
        function_list.append(Sum())
        function_list.append(Mean())
        function_list.append(FindGuidForWTPFamily())
        function_list.append(FindGuidForWTPTwin())
        function_list.append(FindBirthdateForWTPTwin())
        function_list.append(FindAgeForWTPTwin())
        function_list.append(FindGenderForWTPTwin())
        function_list.append(FindBirthdateForWTPFamily())
        function_list.append(FindGenderForWTPFamily())
        function_list.append(FindAgeForWTPFamily())
        return function_list

    def _set_template_structure_(self):
        template_structure = TemplateStructure()
        template_structure.set_to_default_structure()
        template_structure.insert_component(DataTableComponent(), 1)
        return template_structure

    ############################
    # Component behavior delegate method
    #########
    def respond_to_data_table(self, data_table):
        # pass the data_table to wtp_source
        self.source.data_table = data_table
