'''
Super Simple Python Plugins is a minimal framework for implementing plugins in Python programs. There's no setup or anything, just create a directory and put the __init__.py file in it (turning the directory into a module). Any Python source files placed in that directory will be automatically loaded when the module is loaded. The names of the plugins will be put in the __all__ list variable. Beyond that, you can do anything you want with the plugins.

Here's an example of how to use it. Let's assume that there is a single plugins directory, named (logically enough) 'plugins'. Submodules should define a callable object named 'register' that will be invoked when the plug-in is loaded, but it's not required.

import plugins

for name in plugins.__all__:
    plugin = getattr(plugins, name)
    try:
        # see if the plugin has a 'register' attribute
        register_plugin = plugin.register
    except AttributeError:
        # raise an exception, log a message, 
        # or just ignore the problem
        pass
    else:
        # try to call it, without catching any errors
        register_plugin()
'''
from glob import glob
from keyword import iskeyword
from os.path import dirname, join, split, splitext
from inspect import isclass 

basedir = dirname(__file__)

__all__ = []
for name in glob(join(basedir, '*.py')):
    module = splitext(split(name)[-1])[0]
    
    if not module.startswith('_') and module.isidentifier() and not iskeyword(module):
        try:
            __import__(__name__ + '.' + module)
            
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning('Ignoring exception {%s} while loading the %r plug-in.', e ,module)
        else:
            __all__.append(module)
__all__.sort()