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


def call_once_and_cache(f):
    """Only call once this function and cache its result for future use"""

    @wraps(f)
    def wrapper(*args, **kwds):
        if not hasattr(f, '_retval'):
            f._retval = f(*args, **kwds)
        return f._retval
    return wrapper
