#!/usr/bin/python
# -*- coding:UTF-8 -*-
#
# Linux package management tool
# @author: Nicolas Iooss

from linux_packages import LinuxSystem, yield_packages, shrink_deps
import os.path
import sys

linsys = LinuxSystem()
print("Autodetected system %s" % linsys.sysname)

BASEDIR = os.path.abspath(os.path.dirname(__file__))
LISTDIR = os.path.join(BASEDIR, 'lists')
LOCALLIST = os.path.join(BASEDIR, 'local.list')
PATTERNLIST = os.path.join(LISTDIR, linsys.sysname + '.%s.list')

if not os.path.exists(LOCALLIST):
    print("Please create a local file named '%s'" % LOCALLIST)
    print("Read '%s.example' for an example of such a file" % LOCALLIST)
    sys.exit(1)

# Read local list file
listpkgs = set()
for localline in yield_packages(LOCALLIST):
    if localline[0] == '@':
        # Include a file
        listpkgs |= set(yield_packages(PATTERNLIST % localline[1:]))
    else:
        # Package definition
        listpkgs.add(localline)

# Expand list
listpkgs = linsys.expand_pkglist(listpkgs)

# Compute diffs with installed packages
uninstalled_pkgs = listpkgs - linsys.installed_packages
installed_pkgs = linsys.installed_packages - listpkgs

# Output
if uninstalled_pkgs:
    print()
    print("Not yet installed and uninstalled packages:")
    pkgs = shrink_deps(uninstalled_pkgs, linsys.get_deps)
    print('\n'.join(sorted(list(pkgs))))

if installed_pkgs:
    print()
    print("Packages not yet recorded in a list:")
    pkgs = shrink_deps(installed_pkgs, linsys.get_deps)
    print('\n'.join(sorted(list(pkgs))))

if not uninstalled_pkgs and not installed_pkgs:
    print("Everything is up to date :)")
