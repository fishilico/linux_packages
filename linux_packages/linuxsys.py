#!/usr/bin/python
# -*- coding:UTF-8 -*-
#
# Linux system management
# @author: Nicolas Iooss

import logging
import os.path
import sys

from .pkglists import expand_groups, expand_deps
from .tools import object_call_once_and_cache, object_call_indexed_value

logger = logging.getLogger(__name__)


class UnsupportedSystem(Exception):
    pass


class UnimplementedCall(Exception):
    pass


def autodetect_sysname():
    """Autodetect system type by analysing files"""
    # Find OS ID from os-release, if this file exists
    if os.path.exists('/etc/os-release'):
        known_os_id = {
            'arch': 'archlinux',
            'debian': 'debian',
        }
        with open('/etc/os-release', 'r') as os_file:
            for line in os_file:
                if line.startswith('ID='):
                    os_id = line[3:].strip()
                    if os_id in known_os_id:
                        return known_os_id[os_id]
                    else:
                        logger.warn("Unknwon os-release ID %s" % os_id)
    if os.path.exists('/etc/arch-release'):
        return 'archlinux'
    elif os.path.exists('/etc/debian_version'):
        return 'debian'
    elif os.path.exists('/etc/gentoo-release'):
        return 'gentoo'
    raise UnsupportedSystem("System autodetection failed")


class LinuxSystem(object):
    """Manage a Linux system"""

    def __init__(self, sysname=None):
        """Load a system with the given name"""
        self.sysname = sysname or autodetect_sysname()
        self.sysname = self.sysname.lower()

        # Import the module
        pos = __name__.rindex('.')
        modulename = '%s.%s' % (__name__[:pos], self.sysname)
        __import__(modulename)
        self.module = sys.modules[modulename]

    def __str__(self):
        return "LinuxSystem(%s)" % self.sysname

    def _call_module(self, fctname, *args, **kwds):
        """Try to call a function in the module.

        Raise UnimplementedCall if this function does not exist
        """
        # Debuging
        #print("\033[37mCall %s(%s)\033[m" % (fctname, ', '.join(args)))
        if not hasattr(self.module, fctname):
            raise UnimplementedCall()
        return getattr(self.module, fctname)(*args, **kwds)

    @property
    @object_call_once_and_cache
    def installed_packages(self):
        """Set of all installed packages"""
        return self._call_module('get_installed_packages')

    @property
    @object_call_once_and_cache
    def installed_groups(self):
        """Dict of all installed package groups"""
        return self._call_module('get_installed_groups')

    @property
    @object_call_once_and_cache
    def all_groups(self):
        """Set of all package groups"""
        return self._call_module('get_all_groups')

    @object_call_indexed_value
    def get_group_packages(self, group):
        """Get a set of packages of specified group"""
        try:
            if not group in self.all_groups:
                return set()
        except UnimplementedCall:
            pass
        try:
            if group in self.installed_groups:
                return self.installed_groups[group]
        except UnimplementedCall:
            pass
        return self._call_module('get_group_packages', group)

    @property
    @object_call_once_and_cache
    def installed_virtual_packets(self):
        """Get dict of virtual packets"""
        return self._call_module('get_installed_virtual_packets')

    @object_call_indexed_value
    def get_real_package(self, package):
        """Get real package name for virtual packages"""
        try:
            if package in self.installed_virtual_packets:
                return self.installed_virtual_packets[package]
        except UnimplementedCall:
            pass
        try:
            return self._call_module('get_real_package', package)
        except UnimplementedCall:
            return package

    @property
    @object_call_once_and_cache
    def _installed_deps(self):
        """Dict of all installed package dependencies"""
        return self._call_module('get_installed_deps')

    @object_call_indexed_value
    def get_deps(self, package):
        """Get the dependencies of a package"""
        try:
            if package in self._installed_deps:
                return self._installed_deps[package]
        except UnimplementedCall:
            pass
        return self._call_module('get_deps', package)

    def expand_pkglist(self, packages):
        """Expand a package list for this system"""
        # Expand groups
        packages, deleted_pkgs = expand_groups(packages, self.get_group_packages)
        packages = expand_deps(packages, self.get_deps, self.get_real_package)
        return packages - deleted_pkgs
