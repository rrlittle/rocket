import json
import sys
import utils
import os.path

def get_path_finder():
    global path_finder
    return path_finder


# this class is responsible for search the path from the
class PathFinder(object):

    def __init__(self):
        super(PathFinder, self).__init__()
        basedir, filename = utils.split(utils.abspath(__file__))
        self.config_name = os.path.join(basedir, "workspace_path_config.json")
        self.path_dict = self.read_in_path_config(self.config_name)

    def read_in_path_config(self, config_path):
        """
            Recall The config_file looks like this
            {
                "workspace":{
                    "mapping_file_dir":"",
                    ....
                }
            }

        :param config_path:
        :return:
        """

        self.config_name = config_path
        file = open(config_path, "r")
        self.config = json.load(file)
        return self.config["workspace"]

    # It will accept a method that does not require argument to deal with
    # what happened if the specified path key doesn't exist
    def find_path(self,
                  path_key,
                  func_if_key_not_found=lambda path_key, path_dict: print("Key: %s not found"
                                                                         " and not get dealt with"%path_key)):
        try:
            path = self.path_dict[path_key]
            return path
        except KeyError as e:
            print("The Path Finder can't find the requested key: %s" %e)
            new_path = func_if_key_not_found(path_key, self.path_dict)
            self.save_path_config()
            return new_path

    # This one is a public method called by other parts of the program to push the path
    # they specified into the path.
    '''def use_path(self,
                 path_key,
                 func_if_key_not_found=lambda path_key, path_dict: print("Key: %s not found"
                                                                         " and not get dealt with"%path_key)):
        path = self.find_path(path_key, func_if_key_not_found)
        sys.path.insert(0, path)
        print(sys.path)'''

    def save_path_config(self):
        file = open(self.config_name, mode="w+")
        try:
            json.dump(self.config, file)
            return True
        except Exception as e:
            print(e)
            return False

path_finder = PathFinder()