from utils import make_logger, logging, truncfile

debuglog = 'debug.log'
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
    flvl = logging.DEBUG
    )

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


map_log = make_logger('mapping manager',
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





 