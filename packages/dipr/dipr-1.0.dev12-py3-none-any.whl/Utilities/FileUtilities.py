
import os
import stat

from shutil import rmtree


def __del_rw(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)


def force_rmtree(path):
    rmtree(path, onerror=__del_rw)
