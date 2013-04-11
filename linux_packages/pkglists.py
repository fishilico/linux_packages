#!/usr/bin/python
# -*- coding:UTF-8 -*-
#
# Manage package list files
# @author: Nicolas Iooss


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
    return new_pkgs - deleted_pkgs, deleted_pkgs


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
        for pkg in list(new_pkgs):
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


def shrink_deps(pkglist, get_deps):
    """Shrink package list by removing explicit dependencies"""
    pkgs = pkglist
    for pkg in list(pkglist):
        pkgs -= get_deps(pkg)
    return pkgs
