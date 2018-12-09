#!/usr/bin/env python

from sys import argv
from os import strerror
import errno
from re import match

err = argv[1]

# very basic checking
if match('[0-9]+', err):
    err = int(err)
    print("%s: %s" % (errno.errorcode[err], strerror(err)))
elif match('E.+', err):
    e = eval('errno.%s' % err)
    print("%s(%d): %s" % (err, e, strerror(e)))
else:
    print("usage: %s <errno>" % argv[0])
