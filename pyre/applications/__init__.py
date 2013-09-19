#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Application import Application
from AppRunner import AppRunner
from ComponentHarness import ComponentHarness
from Script import Script
from Shell import Shell
from SimpleComponentHarness import SimpleComponentHarness
from SuperScript import SuperScript


def commandlineParser():
    from CommandlineParser import CommandlineParser
    return CommandlineParser()
    

def superCommandlineParser():
    from SuperCommandlineParser import SuperCommandlineParser
    return SuperCommandlineParser()
    

def start(argv=None, **kwds):
    """general-purpose entry point for applications"""
    cls = kwds.get('applicationClass')
    kwds = dict(**kwds)
    kwds['argv'] = argv
    app = cls()
    shell = Shell(app)
    shell.run(**kwds)
    return 0


def loadObject(name):
    """Load and return the object referenced by <name> ==
    some.module[:some.attr].

    Derived from EntryPoint.

    2013-09-19: Extracted from merlin by Brad Aagaard to remove
      dependence of nemesis on merlin.
    """

    module, attrs = name.split(':')
    attrs = attrs.split('.')
    obj = __import__(module, globals(), globals(), ['__name__'])
    for attr in attrs:
        obj = getattr(obj, attr)
    return obj


# version
__id__ = "$Id: __init__.py,v 1.1.1.1 2005/03/08 16:13:49 aivazis Exp $"

# End of file 
