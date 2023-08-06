#!/usr/bin/python3

import sys

# Run the main entry point, similarly to how setuptools d$
# we didn't install the actual entry point from setup.py,$
# pkg_resources API.
import KonbiLockerLite

from KonbiLockerLite import LockerLite

args = sys.argv
if len(args) > 1:
    if args[1].lower() == 'setup':
        LockerLite.setup()
else:
    LockerLite.run()
