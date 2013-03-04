#!/usr/bin/python
# -*- coding:UTF-8 -*-
#
# Linux package management tool
# @author: Nicolas Iooss

from linux_packages import LinuxSystem, load_packages_from_lists
import sys

linsys = LinuxSystem()
print("Autodetected system %s" % linsys.sysname)

if linsys.sysname == 'archlinux':
    listfiles = [
        'common',
        'desktop',
        'devel',
        'games',
        'hacking',
        'server',
        'specific',
        'wireless'
    ]
else:
    print("Unsupported system %s" % linsys.sysname)
    sys.exit(1)

# Get installed packages
installedpkgs = linsys.installed_packages

# Retrieve listed packages and expand this list
listpkgs = load_packages_from_lists('lists', linsys.sysname, listfiles)
listpkgs = linsys.expand_pkglist(listpkgs)

# Output
print()
print("Not yet installed and uninstalled packages:")
pkgs = listpkgs - installedpkgs
print('\n'.join(sorted(list(pkgs))))

print()
print("Packages not yet recorded in a list:")
pkgs = installedpkgs - listpkgs
print('\n'.join(sorted(list(pkgs))))
