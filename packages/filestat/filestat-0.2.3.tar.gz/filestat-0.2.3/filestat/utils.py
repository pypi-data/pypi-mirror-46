#!/usr/bin/python3

import os as _os
from datetime import datetime as _datetime
import pwd as _pwd
import grp as _grp
import getpass as _getpass


def get_user_name() -> str:
    """Return current user name"""
    return _getpass.getuser()


def get_group_name(user: str=None) -> str:
    """Retun current group name for current user"""
    if user is None:
        user = get_user_name()

    group_id = _pwd.getpwnam(user).pw_gid
    return _grp.getgrgid(group_id).gr_name


def get_size(name: str) -> int:
    """A function that return file size in bytes and other format."""
    try:
        stats = _os.stat(name)
    except FileNotFoundError:
        raise FileNotFoundError(f'{name} this file does not exists, make sure you input correct file name.')
    except Exception:
        raise
    return stats.st_size


def get_permissions(name: str) -> int:
    """A function that return file permission in octal as int."""
    try:
        stats = _os.stat(name)
    except FileNotFoundError:
        raise FileNotFoundError(f'{name} this file does not exists, make sure you input correct file name.')
    except Exception:
        raise

    return int(oct(stats.st_mode)[-3:])  # return the last three digits


def get_last_access_time(name: str) -> str:
    """A function that return last access of a file in python datetime 'Sunday, May 05, 2019 06:54:41.533611 PM'"""
    try:
        stats = _os.stat(name)
    except FileNotFoundError:
        raise FileNotFoundError(f'{name} this file does not exists, make sure you input correct file name.')
    except Exception:
        raise

    return _datetime.fromtimestamp(stats.st_atime).strftime("%A, %B %d, %Y %I:%M:%S.%f %p")


def creation_time(name: str) -> str:
    """Function return last modification date or the creation date."""

    try:
        stats = _os.stat(name)
    except FileNotFoundError:
        raise FileNotFoundError(f'{name} this file does not exists, make sure you input correct file name.')
    except Exception:
        raise

    return _datetime.fromtimestamp(stats.st_mtime).strftime("%A, %B %d, %Y %I:%M:%S.%f %p")


def get_owner_info(name: str) -> str:
    """A function that return owner name of a file"""
    try:
        stats = _os.stat(name)
    except FileNotFoundError:
        raise FileNotFoundError(f'{name} this file does not exists, make sure you input correct file name.')
    except Exception:
        raise
    owner = _pwd.getpwuid(stats.st_uid)
    return owner.pw_name


def get_group_info(name: str) -> str:
    """A function that return group info of a file"""
    try:
        stats = _os.stat(name)
    except FileNotFoundError:
        raise FileNotFoundError(f'{name} this file does not exists, make sure you input correct file name.')
    except Exception:
        raise
    group = _grp.getgrgid(stats.st_uid)
    return group.gr_name


def check_owner(owner: str, fp_name: str) -> bool:
    """A function that cross check file owner name"""

    confirm = False
    try:
        if get_owner_info(fp_name) == owner:
            confirm = True
    except FileNotFoundError:
        raise FileNotFoundError(f'{fp_name} this file does not exists, make sure you input correct file name.')
    except Exception:
        raise

    return confirm


def check_group(owner: str, fp_name: str) -> bool:
    """A function that cross check file group name"""

    confirm = False
    try:
        if get_group_info(fp_name) == owner:
            confirm = True
    except FileNotFoundError:
        raise FileNotFoundError(f'{fp_name} this file does not exists, make sure you input correct file name.')
    except Exception:
        raise

    return confirm


def readable(fp_name: str) -> bool:
    confirm = False

    try:
        if _os.access(fp_name, _os.R_OK):
            confirm = True
    except FileNotFoundError:
        raise FileNotFoundError(f'{fp_name} this file does not exists, make sure you input correct file name.')
    except Exception:
        raise

    return confirm


def writable(fp_name: str) -> bool:
    """Function return boolean about the file writable or not!"""

    confirm = False

    try:
        if _os.access(fp_name, _os.W_OK):
            confirm = True
    except FileNotFoundError:
        raise FileNotFoundError(f'{fp_name} this file does not exists, make sure you input correct file name.')
    except Exception:
        raise

    return confirm


def executable(fp_name: str) -> bool:
    """Function return boolean about the file executable or not!"""

    confirm = False

    try:
        if _os.access(fp_name, _os.X_OK):
            confirm = True
    except FileNotFoundError:
        raise FileNotFoundError(f'{fp_name} this file does not exists, make sure you input correct file name.')
    except Exception:
        raise

    return confirm
