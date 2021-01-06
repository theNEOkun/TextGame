import os
import sys
import shutil
import logging
from pathlib import Path
RESOURCES = Path(__file__).parent / "../_RESOURCES/"

COLUMNS, LINES = shutil.get_terminal_size()


def create_logger():
    """ Creates a logging object to be used for reports. """
    '''Creates a standard logger which sends the files to _resources. Since the specifications of the actual message
    is taken care of by the function, the only formatting here is to not write anything else but the message.'''

    save = logging.getLogger("save")
    save.setLevel(logging.DEBUG)

    file_handle = logging.FileHandler(RESOURCES / "save.log", "w")
    file_format = logging.Formatter("%(message)s")
    file_handle.setFormatter(file_format)

    save.addHandler(file_handle)

    logger = logging.getLogger("gol_logger")
    logger.setLevel(logging.INFO)

    file_handle = logging.FileHandler(RESOURCES / "gol.log", "w")
    file_format = logging.Formatter("%(message)s")
    file_handle.setFormatter(file_format)

    logger.addHandler(file_handle)

    return logger, save


def set_console():
    cmd = 'mode 100,50'
    os.system(cmd)


def fancy():
    sys.stdout.write("{0:*^{1}}\n".format("", 100))


def progress(_status: str):
    """ Update progress information in console. """
    sys.stdout.write("{}".format(_status))


def clear_console():
    """ Clear the console. POSIX refers to OSX/Linux. """
    os.system('clear' if os.name == 'posix' else 'cls')