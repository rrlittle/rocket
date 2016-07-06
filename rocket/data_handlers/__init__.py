''' this script is called when this package is imported
	it will look through the package and enumerate all the classes
	found within. 

	if they are subclasses of sinkManager or sourceManager
	they will be saved in either 
	__sinkHandlers__ or __sourceHandlers__
	
	if there is a conflict a dataHandlerImplementationError 
	will be thrown.

	this script implies some rules about the names and structures of 
	your data_handlers
	they should be named common sense things. not python keywords like 'for'
	they also must implement 

'''
from Managers import sourceManager, sinkManager, ssManager
from __init__ import ignore_errors 
from importlib import import_module
from glob import glob
from keyword import iskeyword
from os.path import dirname, join, split, splitext
from inspect import isclass  


__sourceHandlers__ = {}
__sinkHandlers__ = {}

# used to indicate an error with loading files
class dHandlerErr(Exception):pass

def not_collision(classname, thismodule, handlerlist):
	''' this just checks that the classname isn't already in 
		the handler list.
		if theres a collision and ignore_errors is true a error
			message is displayed. and return True 
		if theres a collision and ignore_errors is False an 
			error is raised
	'''
	if classname in handlerlist:
		errstr = (  'name collision in module %s '
					'\nwith module %s'
					'\nplease change one of them')%(
					thismodule, handlerlist[cname])
		if ignore_errors: print(errstr)
		else: raise dHandlerErr(errstr) 
		return False
	return True

def load_module(module_str):
	''' this loads a module object an returns it. for further 
		checking
		if errors occur. will return a dHandlerErr with problem
		to raise or not
	'''
	try:
		# attempt to import the module
		# e.g. import data_handlers.pyfile
		module =import_module(module_str)
		return module
	except Exception as e: # error. ignoring. 
		err = dHandlerErr(('exception {%s} while loading '
				'the %r plug-in.')%(e,module_str))
		return err

def load_classes(module):
	''' given module. 
		look through it's classes and sort them into 
		source and sink managers or drop them
		adds them to 
	'''
	moddic = module.__dict__
	# get the classes within the file
	classes = {k:v for k,v in moddic.items() if isclass(v)}  
	for cname, _class in classes.items():
		if issubclass(_class, sourceManager):
			if not_collision(cname, _class, __sourceHandlers__): 
				__sourceHandlers__[cname] = _class
		if issubclass(_class, sinkManager):
			if not_collision(cname, _class, __sinkHandlers__): 
				__sinkHandlers__[cname] = _class


#################################
## Main

basedir = dirname(__file__) # get this package name
pyfiles = glob(join(basedir, '*.py')) # search for python files
for filepath in pyfiles: # look at each file in turn
	filename = split(filepath)[-1]
	modulename = splitext(filename)[0] # remove .py extension so we can import it
	
	if  (   not modulename.startswith('_') # e.g. __init__.py
			and modulename.isidentifier()  # T iff str module is a var at present
			and not iskeyword(modulename)  # if its a special keyword
		):
		module = load_module(__name__ + '.' + modulename)
		if isinstance(module, dHandlerErr): 
			if ignore_errors: 
				print(module.args[0]) # print err message
				continue # go to next module
			else: raise module # raise exception
		# else module loaded successfully

		load_classes(module)


