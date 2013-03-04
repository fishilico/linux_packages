#!/usr/bin/python
# -*- coding:UTF-8 -*-
#
# Some useful routines that are used is linux_packages
# @author: Nicolas Iooss

from functools import wraps
import subprocess


def process_output(*args):
    """Execute the process command line in args.

    Return list of lines of command output.
    """
    proc = subprocess.Popen(args, stdout=subprocess.PIPE, env={'LANG': 'C'})
    lines = proc.communicate()[0].decode('utf-8').split('\n')
    return [l for l in lines if l]


def object_call_once_and_cache(f):
    """Only call once this function and cache its result for future use"""

    @wraps(f)
    def wrapper(self):
        retkey = '_retval_' + f.__name__
        if not hasattr(self, retkey):
            setattr(self, retkey, f(self))
        return getattr(self, retkey)
    return wrapper


def object_call_indexed_value(f):
    """Only call this function once per argument value, caching result"""

    @wraps(f)
    def wrapper(self, arg):
        retkey = '_retval_' + f.__name__ + '__' + str(arg)
        if not hasattr(self, retkey):
            setattr(self, retkey, f(self, arg))
        return getattr(self, retkey)
    return wrapper
