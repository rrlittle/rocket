from utils import make_logger, logging, truncfile
from __init__ import basedir
from pathlib import Path

#import ipdb; ipdb.set_trace()

debuglog_path = Path(basedir, 'debug.log')
debuglog = str(debuglog_path)
frmt = '%(name)s:%(levelno)s:%(lineno)s:%(message)s'

truncfile(debuglog)

# for logging things in main
mainlog = make_logger('main_log',
    frmt=frmt,
    fpath=debuglog,
    stdout=True,
    # lvl=logging.DEBUG, # use one of the following to easily set the stdout log level
    lvl=logging.INFO,
    # lvl=logging.WARNING,
    # lvl=logging.ERROR,
    # lvl=logging.CRITICAL,
    flvl = logging.INFO
    )

man_log = logging.getLogger("main_log.managers")

'''
man_log = make_logger('managers',
    frmt=frmt,
    fpath=debuglog,
    stdout=True,
    # lvl=logging.DEBUG, # use one of the following to easily set the stdout log level
    lvl=logging.INFO,
    # lvl=logging.WARNING,
    # lvl=logging.ERROR,
    # lvl=logging.CRITICAL,
    flvl = logging.DEBUG
    )
'''

map_log = logging.getLogger("main_log.mappings")

'''
map_log= make_logger('mapping manager',
    frmt=frmt,
    fpath=debuglog,
    stdout=True,
    # lvl=logging.DEBUG, # use one of the following to easily set the stdout log level
    lvl=logging.INFO,
    # lvl=logging.WARNING,
    # lvl=logging.ERROR,
    # lvl=logging.CRITICAL,
    flvl = logging.DEBUG
    )
    '''

col_log = logging.getLogger("main_log.columns")

'''
col_log = make_logger('columns',
    frmt=frmt,
    fpath=debuglog,
    stdout=True,
    # lvl=logging.DEBUG, # use one of the following to easily set the stdout log level
    lvl=logging.INFO,
    # lvl=logging.WARNING,
    # lvl=logging.ERROR,
    # lvl=logging.CRITICAL,
    flvl = logging.DEBUG
    )
    '''

func_log = logging.getLogger('main_log.functions')

control_log = logging.getLogger('main_log.control')
'''
func_log = make_logger('functions',
    frmt=frmt,
    fpath=debuglog,
    stdout=True,
    # lvl=logging.DEBUG, # use one of the following to easily set the stdout log level
    lvl=logging.INFO,
    # lvl=logging.WARNING,
    # lvl=logging.ERROR,
    # lvl=logging.CRITICAL,
    flvl = logging.DEBUG
    )
'''


 