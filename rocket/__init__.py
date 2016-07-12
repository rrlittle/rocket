import utils

# figure out a bunch of directories so we don't need to parse them every time
# Yay abstraction!

home_dir_str = None
if utils.systemName == 'Linux':
	home_dir_str = utils.environ['HOME']
elif utils.systemName == 'Windows':
	try:
		# used by waisman users alone
		home_dir_str = utils.environ['_USR'] + '/'
	except AttributeError:
		home_dir_str = utils.environ['USERPROFILE'] + '/'



basedir,filename = utils.split(utils.abspath(__file__))
basedir = utils.split(basedir)[0]
print('dirname',utils.abspath(utils.dirname(__file__)))
print('file', utils.abspath(__file__))
print('basedir', basedir)

templatedir = utils.join(basedir, 'mapping_files')
srcdatdir = utils.join(basedir,' source_datafiles')
srcschdir = utils.join(basedir,' source_schemes')
sinkdatdir = utils.join(basedir,' sink_datafiles')
sinkschdir = utils.join(basedir,' sink_schemes') 
sectretdir = home_dir_str

# used throughout the package to decide 
# to throw errors or just log them
ignore_errors = False

# loads all the handlers we know about 
# so you can pass one to of each to the controller
handlers = utils.load_handlers()