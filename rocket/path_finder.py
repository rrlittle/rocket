import json
import sys
import utils
import os.path
import logging

def get_path_finder():
    global path_finder
    return path_finder


# this class is responsible for search the path from the
class PathFinder(object):

    def __init__(self):
        super(PathFinder, self).__init__()
        basedir, filename = utils.split(utils.abspath(__file__))
        self.config_name = os.path.join(basedir, "workspace_path_config.json")
        self.logger = logging.getLogger("main_log.path_finder")
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
        self.config = None
        file = open(config_path, "r")
        try:
            self.config = json.load(file)
        except Exception as e:
            self.logger.critical("Error in json file: %s \n "
                                 "Please check whether your file path has consistent double slash '\\\\', "%e)
            raise e
        return self.config["workspace"]

    # It will accept a method that does not require argument to deal with
    # what happened if the specified path key doesn't exist
    # That function will need to accept two arguments: path key and the self.path_dict so that outside can change it
    def find_path(self,
                  path_key,
                  func_if_path_not_found=lambda path_key, path_dict: print("Key: %s not found"
                                                                         " and not get dealt with" % path_key),
                  func_if_path_empty = lambda path_key, path_dict: print("Path is empty")):
        try:
            path = self.path_dict[path_key]
            if path is None:
                raise KeyError("The path is None")

            if path == "":
                path = func_if_path_empty(path_key, self.path_dict)

            if not os.path.exists(path):
                raise KeyError("The path is not a valid path")

            return path
        except KeyError as e:
            print("The Path Finder can't find a valid answer for that path: %s" %e)
            new_path = func_if_path_not_found(path_key, self.path_dict)
            return new_path
        finally:
            self.save_path_config()

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
        #TODO: Make sure that if json.dump throws an exception, the original file will not get changed or erased.
        file = open(self.config_name, mode="w+")
        try:
            json.dump(self.config, file)
            return True
        except Exception as e:
            print(e)
            return False

path_finder = PathFinder()


def test(path_finder):
    path = path_finder.find_path("mapping_file_dir")
    print(path)

test(path_finder)
