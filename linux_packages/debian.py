#!/usr/bin/python
# -*- coding:UTF-8 -*-
#
# Integration with Debian package manager (apt)
# Only operation on local database are supported
#
# Debian has no concept of a package group which installs other packages with
# a selection. It uses instead dependancies.
# Virtual packages provide a functionality, by other packets.
#
# @author: Nicolas Iooss

import apt


# Build package cache
APT_CACHE = apt.Cache()


def get_installed_packages():
    """Get all installed packages on a Debian system"""
    return frozenset([p.name for p in APT_CACHE if p.is_installed])


def get_all_groups():
    """Get a set of all package groups"""
    return frozenset()


def get_installed_groups():
    """Get a dict of all installed package groups"""
    return frozenset()


def get_group_packages(group):
    """Get a set of packages of specified group"""
    return frozenset()


def get_installed_virtual_packets():
    """Get a dict of virtual packets"""
    packages = dict()
    return packages


def get_real_package(package):
    """Get real package name for virtual packages"""
    providers = APT_CACHE.get_providing_packages(package)
    if not providers:
        return package
    return providers[0].name


def get_installed_deps():
    """Get all dependencies of all installed packages"""
    deps = dict()
    for pkg in APT_CACHE:
        if pkg.is_installed:
            # pkg.installed.dependencies is a list of OR-lists of deps
            dpkg_deps = set()
            for dlist in pkg.installed.dependencies:
                or_deps = set()
                for d in dlist:
                    # Only add installed deps
                    if d.name in APT_CACHE and APT_CACHE[d.name].is_installed:
                        or_deps.add(d.name)
                    # Virtual packages
                    if APT_CACHE.is_virtual_package(d.name):
                        or_deps.add(get_real_package(d.name))
                if dlist and not or_deps:
                    print("Unable to resolve dependencies of package %s: %s"
                        % (pkg.name, dlist))
                # Continue even if a dep is missing.
                # This is not a package manager !
                dpkg_deps |= or_deps
            deps[pkg.name] = dpkg_deps
    return deps


def get_deps(package):
    """Get dependencies of a package, mixing"""
    deps = set()
    if package not in APT_CACHE:
        print("Unknown package %s" % package)
        return deps

    for dlist in APT_CACHE[package].candidate.dependencies:
        or_deps = set()
        for d in dlist:
            # Only add installed deps
            if d.name in APT_CACHE and APT_CACHE[d.name].is_installed:
                or_deps.add(d.name)
            # Virtual packages
            if APT_CACHE.is_virtual_package(d.name):
                or_deps.add(get_real_package(d.name))
        # Continue even if a dep is missing.
        # This is not a package manager !
        deps |= or_deps
    return deps
