# Autogenerated by Astropy-affiliated package astropy_helpers's setup.py on 2018-12-31 23:55:32 UTC
from __future__ import unicode_literals
import datetime

version = "3.1"
githash = "9f82aac6c2141b425e2d639560f7260189d90b54"


major = 3
minor = 1
bugfix = 0

version_info = (major, minor, bugfix)

release = True
timestamp = datetime.datetime(2018, 12, 31, 23, 55, 32)
debug = False

astropy_helpers_version = ""

try:
    from ._compiler import compiler
except ImportError:
    compiler = "unknown"

try:
    from .cython_version import cython_version
except ImportError:
    cython_version = "unknown"
