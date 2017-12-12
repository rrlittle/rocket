from MappingManager import MappingManager
from data_handlers import coins, ndar
from Functions import ursi_functions
from loggers import map_log
from __init__ import templatedir, secretdir
from Functions.calc_functions import Mean, Sum, FindFirstValid, TestNoData, ReverseBySubtractingFrom, Subtract, MaxLength,\
                                      ConcatString
from tkinter import filedialog, messagebox
#from Functions.ursi_functions import FindAge, FindBirthdate, FindGender, FindGuid, FindGuidByWBIC, FindAgeByWBIC,\
#                                    FindBirthdateByWBIC,FindGenderByWBIC
from Functions.ursi_functions import FindGuid, FindGuidByWBIC, FindUrsiByWBIC
from Functions.personal_info_functions import FindAge, FindBirthdate, FindGender
from Functions.wbic_functions import FindBirthdateByWBIC, FindAgeByWBIC, FindGenderByWBIC

from Functions.subject_01_extension import GetCommentMisc, GetCotwinGuid, GetMotherGuid, GetCotwinCommentMotherUrsi
from Functions.bdi_extension import GetBDIScore
from Functions.interview_functions import GenderResponse

from __init__ import templatedir, sinkdatdir, srcdatdir, ndartempdir
from utils.ndar_template_parser import NdarTemplateParser, CoinsDataParser
from typing import *
from utils.ndar_template_parser import NdarElement
from pathlib import Path
from tkinter import messagebox, Tk, simpledialog
from template_kit.TemplateComponents import MappingInfo, InstruInfo, InstruInfoComponent

class coins2ndar(MappingManager):
    ''' this manager is to define the mappping between coins and ndar type files.
    '''

    def __init__(self):
        ''' this initializes a mapping manager with coins as source and ndar as sink
        '''
        MappingManager.__init__(self,
                                source=coins.coins_src,
                                sink=ndar.ndar_snk)
        # print('functions', self.globalfuncs)
        #ursi_data_manager = ursi_functions.UrsiDataManager(secretdir)

    def load_functions(self):
        functions_list = []
        functions_list.append(Mean())
        functions_list.append(Sum())
        functions_list.append(Subtract())
        functions_list.append(MaxLength())
        functions_list.append(ConcatString())
        functions_list.append(GenderResponse())

        functions_list.append(FindAge())
        functions_list.append(FindAgeByWBIC())
        functions_list.append(FindBirthdate())
        functions_list.append(FindBirthdateByWBIC())
        functions_list.append(FindGender())
        functions_list.append(FindGenderByWBIC())

        functions_list.append(FindGuid())
        functions_list.append(FindGuidByWBIC())
        functions_list.append(FindUrsiByWBIC())
        functions_list.append(GetCommentMisc())
        functions_list.append(GetCotwinCommentMotherUrsi())
        functions_list.append(GetMotherGuid())
        functions_list.append(GetCotwinGuid())
        functions_list.append(GetBDIScore())
        functions_list.append(FindFirstValid())
        functions_list.append(TestNoData())
        functions_list.append(ReverseBySubtractingFrom())

        return functions_list
    '''
        functions['mean'] = {'ref': func.mean, 'doc':"Calculate the mean. Put the coins ids "
                                                     "for all the columns into the mapping id"}
        functions['sum'] = {'ref': func.sum, 'doc':"Calculate the sum. Put the coins ids for all"
                                                   " the columns into the mapping id"}
        functions['findGender'] = {'ref': ursi_functions.findGender, 'doc': "Find the participant's gender based "
                                                                            "on ursi"}
        functions['findGuid'] = {'ref': ursi_functions.findGuid, 'doc': "Find the participants's GUID based "
                                                                       "on the given ursi"}
        functions['findMotherGuidS1'] = {'ref': s1.get_mother_guid}
        functions['findAge'] = {'ref': findAge, 'doc': "Find the participants's Age based "
                                            "on the given ursi, and assessment date. Put two coins id into the mapping id."
                                                      "Like 1,4"}
        functions['findCotwinGuidS1'] = {'ref': s1.get_cotwin_guid, 'doc': "Subjective01 Extension: Given one child's ursi, "
                                                                           "it will return his or her cotwin's GUID. "
                                                                           "PLEASE put subject01 file name into the args!"}
        functions['findCommentsS1'] = {'ref': s1.get_comment_misc, 'doc':"Subjective01 Extension: Given one child's ursi,"
                                                                           "it will return the comment about her in Subjective 01 "
                                                                         "PLEASE put subject01 file name into the args!"}
        functions['findCommentMotherS1'] = {'ref': s1.get_cotwoin_comment_based_on_mother_ursi,
                                            'doc': "Subjective01 Extension: Given mother's ursi, it will return "
                                                   "comment containing her twins GUID information. "
                                                   "PLEASE put subject01 file name into the args!"}
                                                   '''

    def want_update_ursi_data(self):
        yes = 'y'
        no = 'n'
        while True:
            user_in = input("The personal data from Coins has already been downloaded,"
                            "do you want to redownload it? (y/n) ")
            if user_in[0].lower == yes:
                return True
            elif user_in[0].lower == no:
                return False

    # Extension method to configure writing template
    def before_write_instru_info(self, instru_info: InstruInfoComponent):
        self.before_write_instru_info(instru_info)
        root = Tk()
        root.withdraw()

        name = simpledialog.askstring("Action", "Enter NDAR instrument name")
        version = simpledialog.askstring("Action", "Enter NDAR instrument version")

        # No input check right now
        instru_info.instru_info.instru_name = name
        instru_info.instru_info.version = version

        root.destroy()

    def add_extra_content_to_mapping_info(self, mapping: MappingInfo) -> None:
        super().add_extra_content_to_mapping_info(mapping)

        # find initial
        ndar_template, coins_data = self._get_ndar_template_and_coins_data_path_()

        if ndar_template is not None:
            ndar_elements = NdarTemplateParser.get_columns(ndar_template)
            ndar_cols = [e.col_name for e in ndar_elements]
        else:
            ndar_cols = []

        # Need error checking
        # parse data file, get sink column
        if coins_data is not None:
            coins_col = CoinsDataParser.get_columns(coins_data)
        else:
            coins_col = []

        # add columns to data file with id.
        mapping_header = self._add_mapping_headers_from_src_sink()
        coins_col_id_index = mapping_header.index(self.source.template_fields["id"])
        coins_col_name_index = mapping_header.index(self.source.template_fields["col_name"])
        coins_missing_value_index = mapping_header.index(self.source.template_fields["missing_vals"])

        ndar_col_id_index = mapping_header.index(self.sink.template_fields["id"])
        ndar_col_name_index = mapping_header.index(self.sink.template_fields["col_name"])
        ndar_default_index = mapping_header.index(self.sink.template_fields["default"])

        longest = max(len(coins_col), len(ndar_cols))
        # the index starts from 1, for user convenience
        for index in range(1, longest+1):
            # fill in each section
            row = [""]*len(mapping_header)  # type:List[str]
            if index <= len(coins_col):
                row[coins_col_id_index] = index
                row[coins_col_name_index] = coins_col[index-1]
                row[coins_missing_value_index] = "~<userSkipped>~,~<condSkipped>~,"

            if index <= len(ndar_cols):
                row[ndar_col_id_index] = index
                row[ndar_col_name_index] = ndar_cols[index-1]
                row[ndar_default_index] = ""

            mapping.content.append(row)

    # Validate tsv and csv as well
    def _get_ndar_template_and_coins_data_path_(self) -> Tuple[str, str]:

        ndar_template = None
        coins_data = None
        messagebox.showinfo("Next step", "Then please choose a NDAR template. "
                                         "\nIf you don't want. you can press cancel on next page")
        while True:
            ndar_template = filedialog.askopenfilename(initialdir=ndartempdir, title="Choose a NDAR template")

            if ndar_template is None or ndar_template == "":
                ndar_template = None
                break

            p = Path(ndar_template)
            if p.suffix != '.csv':
                messagebox.showwarning("File error", "Please choose a csv file .")
                pass
            else:
                break

        messagebox.showinfo("Next step", "Then please choose a COINS data file"
                                         "\n if you don't want. you can press cancel on next page")
        while True:
            coins_data = filedialog.askopenfilename(initialdir=srcdatdir, title="Choose a coins data file")

            if coins_data is None or coins_data == "":
                coins_data = None
                break
            p = Path(coins_data)
            if p.suffix != '.tsv' and p.suffix != '.csv':
                messagebox.showwarning("File error", "Please choose a tsv or txt file")
                pass
            else:
                break

        return ndar_template, coins_data