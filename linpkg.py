#!/usr/bin/python
# -*- coding:UTF-8 -*-
#
# Linux package management tool
# @author: Nicolas Iooss

from linux_packages import LinuxSystem, load_packages_from_lists

listfiles = ['common', 'desktop']

linsys = LinuxSystem()
print("Autodetected system %s" % linsys.sysname)

# Get installed packages
installedpkgs = linsys.installed_packages

# Retrieve listed packages and expand this list
listpkgs = load_packages_from_lists('lists', linsys.sysname, listfiles)
listpkgs = linsys.expand_pkglist(listpkgs)
print(sorted(list(listpkgs)))
