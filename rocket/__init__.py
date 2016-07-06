import utils

basedir = utils.abspath(__file__)
templatedrir = utils.join(basedir, 'mappping_files')
srcdatdir = utils.join(basdir, 'source_datfiles')
srcschdir = utils.join(basedir,'source_schemes')
sinkdatdir = utils.join(basedir, 'sink_datfiles')
sinkschdir = utils.join(basedir, 'sink_schemes') 

# used throughout the package to decide 
# to throw errors or just log them
ignore_errors = False

# loads all the handlers we know about 
# so you can pass one to of each to the controller
handlers = utils.load_handlers()