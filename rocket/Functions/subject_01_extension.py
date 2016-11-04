import csv
from os.path import split, join
from path_finder import get_path_finder
from tkinter import filedialog
import logging


s1_logger = logging.getLogger("main_log.subject01_extension")

def get_subject01Manager():
    global subject01Manager
    return subject01Manager


class Subject01NotFoundError(FileNotFoundError): pass


class Subject01InfoNotFound(ValueError): pass


class Subject01DataManager(object):
    """This manager is going to be responsible for storing different small databases
    for the whole project.
    It will also be responsible for tracking which subject01 user is using
    This will also be a singleton for each time rocket runs as long as the user wants to use the method
    It will also notify the path finder that it wants to use the subject01 directory for those subject01
    If it can't find it, it will ask the user to choose a directory
    """

    def __init__(self):
        super(Subject01DataManager, self).__init__()
        self.databases = []
        self.path_key = "subject01_dir"
        self.subject01_dir = ''

        # notify the path finder to use subject01 path
        self.use_path_in_config()

    def use_path_in_config(self):
        '''
        This method is used to add path key for path_dict to update the key
        :return:
        '''
        def if_path_not_found(path_key, path_dict):
            dir_path = filedialog.askdirectory(title="Please choose the directory for your subject file")
            path_dict[path_key] = dir_path
            return dir_path

        path_finder = get_path_finder()
        self.subject01_dir = path_finder.find_path(self.path_key, if_path_not_found)

    def get_subject01_db(self, file_path):
        '''
        Given a file_path, this method will find the corresponding db in the list of database
        :param file_path:
        :return:
        '''
        if self.databases_is_empty():
            return self.add_new_database_to_manager(file_path, self.subject01_dir)
        else:
            db = self.search_db_in_dbs(filename=self.get_filename_from_path(file_path))
            if db == None:
                # If I can't find the database based on the filename, I will create another new db
                return self.add_new_database_to_manager(file_path)
            else:
                return db

    def search_db_in_dbs(self, filename):
        for db in self.databases:
            if db.filename == filename:
                return db
        return None

    def add_new_database_to_manager(self, file_path, s1file_dir):
        '''
        This adds the new database to the managers
        :param file_path: new_subject01_filepath. It can be an absolute path, or just a filename
        :param s1file_dir: the directory for the s1file specified in path finder
        :return:
        '''
        new_db = SubjectInfoDatabase(file_path, s1file_dir)
        self.databases.append(new_db)
        return new_db

    def databases_is_empty(self):
        return len(self.databases) == 0

    def get_filename_from_path(self, path):
        return split(path)[-1]


class SubjectInfoDatabase(object):
    def __init__(self, file_path, s1file_dir = ''):
        super(SubjectInfoDatabase, self).__init__()
        self.file_path = file_path
        self.filename = self.get_filename_from_path(
            self.file_path)  # file name will be used in the future to compare different file database
        self.ursi_key = "src_subject_id"  # This key is used to find the ursi
        self.datatable = {}
        self.s1file_dir = s1file_dir

        self.read_datafile_into_datatable(self.file_path)

    # I assueme there will be two ways of user input file directory: One is that the
    # user will just give a filename, because they have set up the configuration file
    # or the user can just give a absolute path.
    def read_datafile_into_datatable(self, file_path):

        # Two ways of reading file are implemented in open_subject01_file
        # if subject01_file can't be found, the method will throw an Subject01NotFound exception
        # I expect this method to crash with that Error
        subject01_file = self.open_subject01_file(file_path)

        # It's essential that the file that user enters is in the right format as ndars requires
        # In the ndar files, the first line is always used to explain which table and version it is
        if self.check_right_subject_01_format(subject01_file):
            reader = csv.DictReader(subject01_file)

            # I'm going to use ursi key to label the row,
            # it will make the future easy to search
            for row in reader:
                ursi = row[self.ursi_key]
                self.datatable[ursi] = row

    def open_subject01_file(self, user_entered_file_path):
        """
        I will use dir + file_path first.
        Then if it doesn't work well, then just use file_path
        If the program still can't find the file, throw exception
        :param file_path:
        :return:
        """

        try:
            file_path_with_dir = join(self.s1file_dir, user_entered_file_path)
            subject01_file = open(file_path_with_dir, 'r', errors="replace")
            return subject01_file
        except FileNotFoundError as e:
            print("The file can't be found with the "
                  "directory given by the configuration file")

        try:
            subject01_file = open(user_entered_file_path, 'r', errors="replace")
            return subject01_file
        except FileNotFoundError as e:
            raise Subject01NotFoundError("No file has been found, please check what you have entered")

    def check_right_subject_01_format(self, subject01_file):
        '''
        Ndar subject 01 file has a standard format start with the first line "ndar_subject,1"
        :param subject01_file: the file object
        :return:
        '''
        reader = csv.reader(subject01_file)

        # only read the first line to test whether this is a subject 01 file
        for row in reader:
            if "ndar_subject" in row:
                return True
            else:
                raise Subject01NotFoundError("The format of selected file is not subject 01 format,"
                                             "please check again")

    def get_filename_from_path(self, file_path):
        return split(file_path)[-1]

    # The other will use this method to find the information for a specific field.
    # It's necessarily to pass a the key for the string
    def find_column_based_on_ursi(self, ursi, info_key):
        row = []
        data = ""
        try:
            row = self.datatable[ursi]
        except KeyError as e:
            print("The ursi: %s is missing, please check whether this ursi exists" % e)
            raise Subject01InfoNotFound("Data can't be found in the subject 01")

        try:
            data = row[info_key]
        except KeyError as e:
            print("The key: %s can't found in the subject key, please call the programmer to check whether the key"
                  "for the function is right" % e)
            raise Subject01InfoNotFound("Data can't be found in the subject 01")
        pass
        return data

    def find_childs_for_a_mother_ursi(self, mother_ursi, mother_key ="src_mother_id", child_num=2):
        childs = []
        for child_ursi, row in self.datatable.items():
            try:
                if row[mother_key] == mother_ursi:
                    childs.append(child_ursi)

                    if len(childs) == child_num:
                        return childs

            except KeyError as e:
                print("Can't locate the mother ursi by mother key, please call the programmer")
                raise Subject01InfoNotFound("Data can't be found in the subject 01")

        print("We can't find enough childs based on mother ursi")
        raise Subject01InfoNotFound("You can't find child based on mother ursi")

 # This method is a highly customized data, but can't guarantee
        #  to get the cleaned data by the program
def get_data_from_column(ursi, args):
    subject01_path = args[0]
    data_key = args[1]
    db = get_subject01Manager().get_subject01_db(subject01_path)
    return db.find_column_based_on_ursi(ursi, data_key)

# the subject01_path
def get_guid(ursi, args=None):
    subject01_path = args[0]
    guid_key = "subjectkey"
    db = get_subject01Manager().get_subject01_db(subject01_path)
    ndar_guid = db.find_column_based_on_ursi(ursi, guid_key)
    return ndar_guid


def get_someone_id(ursi, args = None, search_key = "", type="m"):
    subject01_path = args[0]
    db = get_subject01Manager().get_subject01_db(subject01_path)
    search_result = db.find_column_based_on_ursi(ursi, search_key)

    if type == "g":
        if is_valid_guid(search_result):
            return search_result
        else:
            raise Subject01NotFoundError("The data is not in NDAR GUID format")
    elif type == "u":
        if is_valid_ursi(search_result):
            return search_result
        else:
            raise Subject01NotFoundError("The data is not in COINS URSI format")
    elif type == "m":
        return search_result


def get_mother_guid(ursi, args=None):
    mother_key = "subjectkey_mother"
    return get_someone_id(ursi, args=args, search_key=mother_key, type="g")


def get_cotwin_guid(ursi, args = None):
    cotwin_key = "subjectkey_sibling1"
    return get_someone_id(ursi, args=args, search_key=cotwin_key, type="g")


def is_valid_guid(guid_candidate):
    if guid_candidate[:4] == "NDAR":
        return True
    return False


def is_valid_ursi(ursi_candidate):
    if ursi_candidate[:1] == "M":
        return True
    return False


#
def get_comment_misc(ursi, args=None):
    comment_key = "comments_misc"
    return get_someone_id(ursi, args=args, search_key=comment_key)


def get_cotwoin_comment_based_on_mother_ursi(mother_ursi, args=None):
    comment_key = "comments_misc"
    subject01_path = args[0]
    db = get_subject01Manager().get_subject01_db(subject01_path)
    child_ursis = db.find_childs_for_a_mother_ursi(mother_ursi=mother_ursi, child_num=1)
    return get_someone_id(child_ursis[0], args=args, search_key=comment_key)

def test():
    data = get_cotwoin_comment_based_on_mother_ursi("M53721739",["rdoc_subject01_data_20160623.csv"])
    print(data)

subject01Manager = Subject01DataManager()
