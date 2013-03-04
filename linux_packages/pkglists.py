#!/usr/bin/python
# -*- coding:UTF-8 -*-
#
# Manage package list files
# @author: Nicolas Iooss

import os.path


def yield_packages(filename):
    """Yield a package names from a filename"""
    for line in open(filename, 'r'):
        line = line.strip()

        # Remove comments
        pos = line.find('#')
        if pos >= 0:
            line = line[0:pos].strip()

        # Yield non-empty lines, which are package names
        if line:
            yield line


def yield_packages_from_pattern_files(filelist, path_pattern=None):
    """Yield a package names from a generated filenames list"""
    for file in filelist:
        filename = (path_pattern % file) if path_pattern else file
        for package in yield_packages(filename):
            yield package


def load_packages_from_lists(listdirpath, sysname, files):
    """Retrieve package names from list names in a directory"""
    pattern = os.path.join(listdirpath, sysname + '.%s.list')
    return yield_packages_from_pattern_files(files, pattern)


def expand_groups(pkglist, get_group_packages):
    """Expand groups into their packages in the list

    get_group_packages is a function: group->set of packages
    """
    new_pkgs = set()
    deleted_pkgs = set()
    for pkg in pkglist:
        if not pkg:
            continue
        if pkg[0] == '!':
            # !package means explicit deletion, after a package is selected
            # by a group
            deleted_pkgs.add(pkg[1:])
        else:
            packages = get_group_packages(pkg)
            if packages:
                new_pkgs |= packages
            else:
                new_pkgs.add(pkg)
    return new_pkgs - deleted_pkgs


def expand_deps(pkglist, get_deps, get_real_package=None):
    """Expand each package with its dependencies

    get_deps is a function: package->set of packages, which are the deps
    get_real_package is a function: package->real package name
    """
    current_pkglist = pkglist
    new_pkgs = pkglist
    while new_pkgs:
        # Get deps of each package in new_pkgs and fill next_new_pkgs
        next_new_pkgs = set()
        for pkg in new_pkgs:
            if get_real_package:
                real_pkg = get_real_package(pkg)
                if real_pkg and real_pkg != pkg:
                    current_pkglist.remove(pkg)
                    current_pkglist.add(real_pkg)
                    pkg = real_pkg
            deps = get_deps(pkg)
            # Keep only deps which are not yet in current package list
            next_new_pkgs |= deps - current_pkglist
        new_pkgs = next_new_pkgs
        current_pkglist |= new_pkgs
    return current_pkglist
