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
from Stager import Stager


class Script(Application, Stager):


    def __init__(self, name):
        Application.__init__(self, name)
        Stager.__init__(self)
        return


    def run(self, *args, **kwds):
        
        # Fire-up pdb and IPython when an exception occurs -- if IPython is available.
        try:
            import sys, IPython.ultraTB
            if sys.stderr.isatty():
                colorScheme = 'Linux'
            else:
                colorScheme = 'NoColor'
            if sys.stdin.isatty() and sys.stdout.isatty() and sys.stderr.isatty():
                callPdb = 1
            else:
                callPdb = 0
            sys.excepthook = IPython.ultraTB.FormattedTB(mode='Verbose', color_scheme=colorScheme, call_pdb=callPdb)
        except ImportError:
            pass

        return super(Script, self).run(*args, **kwds)


# version
__id__ = "$Id: Script.py,v 1.3 2005/03/10 06:06:37 aivazis Exp $"

# End of file 
