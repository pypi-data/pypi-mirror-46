# -*- coding: utf-8 -*-

"""
DIALS Dependency meta-package
https://github.com/dials/dials-dependencies
"""

from __future__ import absolute_import, division, print_function

__all__ = ["version", "version_tuple"]

version = "0.7.0"
version_tuple = tuple(int(x) for x in version.split("."))
