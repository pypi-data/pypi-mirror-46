#!/usr/bin/python3

import sys

# Run the main entry point, similarly to how setuptools d$
# we didn't install the actual entry point from setup.py,$
# pkg_resources API.
import KonbiLockerLite

from KonbiLockerLite import LockerLite

LockerLite.run()