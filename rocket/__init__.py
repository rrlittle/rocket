from tkinter import filedialog

import utils
import os
import sys
from path_finder import path_finder

# add self path to system path
dirname = os.path.dirname(__file__)
sys.path.insert(0, dirname)

# define soe global stuff

# figure out a bunch of directories so we don't need to parse them every time
# Yay abstraction!
waisman_user = False
home_dir_str = None
if utils.systemName in ('Linux', 'Darwin'):
    home_dir_str = utils.environ['HOME']
elif utils.systemName == 'Windows':
    try:
        # used by waisman users alone
        home_dir_str = utils.environ['_USR'] + '/'
        waisman_user = True
    except (AttributeError, KeyError):
        home_dir_str = utils.environ['USERPROFILE'] + '/'

basedir, filename = utils.split(utils.abspath(__file__))  # within the package

basedir = utils.split(basedir)[0]  # move up one dir


def if_path_not_found(path_key, path_dict):
    dir_path = filedialog.askdirectory(title="Please choose the directory for your %s file"%path_key)
    path_dict[path_key] = dir_path
    return dir_path

#templatedir = utils.join(basedir, 'mapping_files')
templatedir = path_finder.find_path("mapping_file_dir", func_if_path_not_found=if_path_not_found
                                    , func_if_path_empty=if_path_not_found)
srcdatdir = path_finder.find_path("source_data_dir", func_if_path_not_found=if_path_not_found
                                    , func_if_path_empty=if_path_not_found)
sinkdatdir = path_finder.find_path("sink_data_dir", func_if_path_not_found=if_path_not_found,
                                   func_if_path_empty=if_path_not_found)


#srcdatdir = utils.join(basedir, 'source_datafiles')
srcschdir = utils.join(basedir, 'source_schemes')
#sinkdatdir = utils.join(basedir, 'sink_datafiles')
sinkschdir = utils.join(basedir, 'sink_schemes')
secretdir = home_dir_str
scriptdir = utils.join(basedir, 'rocket', 'lib', 'scripts')

# used throughout the package to decide 
# to throw errors or just log them
ignore_errors = False

#  the delimiter for template files. it's here to make it global
templ_delimiter = ','

# actually do stuff....

# loads all the handlers we know about 
# so the mapping managers can select them
handlers = utils.load_handlers()

# loads all the mapping managers we know about 
# so you can pass one to the controller
mapping_managers = utils.load_map_submanagers()
