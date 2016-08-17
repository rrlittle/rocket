import utils

# define soe global stuff

# figure out a bunch of directories so we don't need to parse them every time
# Yay abstraction!
waisman_user = False
home_dir_str = None
if utils.systemName in ('Linux','Darwin'):
	home_dir_str = utils.environ['HOME']
elif utils.systemName == 'Windows':
	try:
		# used by waisman users alone
		home_dir_str = utils.environ['_USR'] + '/'
		waisman_user = True
	except (AttributeError,KeyError):
		home_dir_str = utils.environ['USERPROFILE'] + '/'



basedir,filename = utils.split(utils.abspath(__file__))  #  within the package
basedir = utils.split(basedir)[0] # move up one dir

templatedir = utils.join(basedir, 'mapping_files')
srcdatdir = utils.join(basedir,'source_datafiles')
srcschdir = utils.join(basedir,'source_schemes')
sinkdatdir = utils.join(basedir,'sink_datafiles')
sinkschdir = utils.join(basedir,'sink_schemes') 
secretdir = home_dir_str
scriptdir = utils.join(basedir, 'rocket','lib','scripts')

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

