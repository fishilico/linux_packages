#!/usr/bin/python
# -*- coding:UTF-8 -*-
#
# Integration with ArchLinux package manager (pacman)
# Only operation on local database are supported
# @author: Nicolas Iooss

from . import tools


def get_installed_packages():
    """Get all installed packages on an ArchLinux system"""
    return frozenset(tools.process_output('pacman', '-Qq'))


def get_all_groups():
    """Get a set of all package groups"""
    return frozenset(tools.process_output('pacman', '-Sqg'))


def get_installed_groups():
    """Get a dict of all installed package groups"""
    groups = dict()
    for line in tools.process_output('pacman', '-Qqg'):
        group, package = line.split(' ', 1)
        if group in groups:
            groups[group].add(package)
        else:
            groups[group] = set([package])
    return groups


def get_group_packages(group):
    """Get a set of packages of specified group"""
    return frozenset(tools.process_output('pacman', '-Sqg', group))


def get_installed_virtual_packets():
    """Get a dict of virtual packets"""
    packages=dict()
    for line in tools.process_output('expac', '%n;%P'):
        if line[-1] == ';':
            pkg = line[0:-1]
            packages[pkg] = pkg
        else:
            real, virt = line.split(';', 1)
            packages[real] = real
            for vpkg in virt.split(' '):
                packages[vpkg] = real
    return packages


def get_real_package(package):
    """Get real package name for virtual packages"""
    for line in tools.process_output('expac', '%n', package):
        return line
    return package


def get_installed_deps():
    """Get all dependencies of installed packages"""
    deps = dict()
    for pkgline in tools.process_output('expac', '%n: %E'):
        pkg, dependent_pkg = pkgline.split(':', 1)
        deps[pkg] = frozenset(dependent_pkg.split())
    return deps


def get_deps(package):
    """Get dependencies of a package"""
    deps = set()
    for line in tools.process_output('pacman', '-Sqi', package):
        if not line.startswith('Depends On'):
            continue
        # Remove 'Depends On   :' prefix
        line = line[line.find(':') + 1:]
        # split with spaces
        for pkg in line.split(' '):
            if not pkg:
                continue
            # Remove version strings
            for char in '<', '=', '>':
                if char in pkg:
                    pkg = pkg[0:pkg.find(char)]
            deps.add(pkg)
    return deps
