from platform import system
from os import environ
from ursi_data_manager import UrsiDataManager
import utils
import logging

def prepare_home_dir():
    home_dir_str = ""  # The home directory for this user account
    system_name = system()
    if system_name in ('Linux', 'Darwin'):
        home_dir_str = environ['HOME']
    elif system_name == 'Windows':
        try:
            # used by waisman users alone
            home_dir_str = environ['_USR'] + '/'
            waisman_user = True
        except (AttributeError, KeyError):
            home_dir_str = environ['USERPROFILE'] + '/'

    return home_dir_str

def prepare_script_path(func_log, scriptdir):
    get_ppi_script_ext = None
    if utils.systemName in ('Linux', 'Darwin'):  # use the
        get_ppi_script_ext = '.sh'
    elif utils.systemName in ('Windows'):  #
        get_ppi_script_ext = '.bat'
    else:
        func_log.critical('This platform is not supported!')
        utils.exit()

    ppi_script_filename = 'list_gender_birth_guid' + get_ppi_script_ext
    ppi_script_path = utils.join(scriptdir, ppi_script_filename)
    func_log.info('ppi script is %s' % ppi_script_path)
    return ppi_script_path

def update_ursi_info(basedir, func_log):
    # I hard code the base dir here
    secret_dir = prepare_home_dir()
    scriptdir = utils.join(basedir, 'rocket', 'lib', 'scripts')
    ppi_script = prepare_script_path(func_log, scriptdir)
    print(scriptdir)
    # This will ask the ursi data manager to update things
    ursi_data_manager = UrsiDataManager(secret_dir_path=secret_dir, first_time_enter=True, ppiscript=ppi_script,
                                        PPIfilename="coinsPersonal.tmp")


def test():
    logger = logging.getLogger("ursi_func")
    basedir = "Q:\\Source_Code\\rocket\\rocket\\"
    update_ursi_info(basedir=basedir, func_log=logger)

test()