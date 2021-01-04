import os
import sys
import shutil

COLUMNS, LINES = shutil.get_terminal_size()


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