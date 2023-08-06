import os
from pathlib import Path


def install_win():

    Path(Path(os.path.expanduser('~')).root +
         "lockerlite.txt").write_text(Path('KonbiLockerLite/install/lockerlite_linux.py').read_text())


def install_linux():
    print('running install_linux')
    print(Path('KonbiLockerLite/install/lockerlite_linux.py').absolute())
    Path("/usr/bin/lockerlite").write_text(
        Path('KonbiLockerLite/install/lockerlite_linux.py').read_text())


def install():
    # create execution entry
    if os.name == 'nt':
        install_win()
    elif os.name == 'posix':
        install_linux()


Path().root
