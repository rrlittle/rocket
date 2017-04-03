from MappingManager import MappingManager
from data_handlers import coins, ndar
from Functions import ursi_functions
from loggers import map_log
from __init__ import templatedir, secretdir
from Functions.calc_functions import Mean, Sum, FindFirstValid, TestNoData, ReverseBySubtractingFrom
#from Functions.ursi_functions import FindAge, FindBirthdate, FindGender, FindGuid, FindGuidByWBIC, FindAgeByWBIC,\
#                                    FindBirthdateByWBIC,FindGenderByWBIC
from Functions.ursi_functions import FindGuid, FindGuidByWBIC, FindUrsiByWBIC
from Functions.personal_info_functions import FindAge, FindBirthdate, FindGender
from Functions.wbic_functions import FindBirthdateByWBIC, FindAgeByWBIC, FindGenderByWBIC

from Functions.subject_01_extension import GetCommentMisc, GetCotwinGuid, GetMotherGuid, GetCotwinCommentMotherUrsi
from Functions.bdi_extension import GetBDIScore

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
