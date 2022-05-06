import CODE.InputOutput as InOut

RESOURCES = InOut.RESOURCES

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

    screen = logging.getLogger("screen")
    screen.setLevel(logging.DEBUG)

    file_handle = logging.FileHandler(RESOURCES / "screen.log", "w")
    file_format = logging.Formatter("%(message)s")
    file_handle.setFormatter(file_format)

    screen.addHandler(file_handle)

    return logger, save, screen
