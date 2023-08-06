import os
from pathlib import Path


def install_win():
    #Path(Path(os.path.expanduser('~')).root + "txt.txt").write_text('test')
    pass


def install_linux():

    Path("/usr/bin/lockerlite").write_text(Path('lockerlite_linux.py').read_text())


def install():
    # create execution entry
    if os.name == 'nt':
        install_win()
    elif os.name == 'posix':
        install_linux()


Path().root
