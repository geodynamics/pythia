#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from ExceptHook import ExceptHook


# facilities and components

def facility(name, **kwds):
    from pyre.inventory.Facility import Facility
    kwds['vault'] = kwds.get('vault', ['hooks'])
    kwds['family'] = kwds.get('family', 'hook')
    return Facility(name, **kwds)


# odb factories

def builtInExceptHook():
    import sys
    return ExceptHook(sys.__excepthook__)


def currentExceptHook():
    import sys
    return ExceptHook(sys.excepthook)


def ultraTBExceptHook():

    try:
        import IPython.ultraTB
    except ImportError:
        return None


    from pyre.components import Component


    class ultraTB(Component):


        name = "ultraTB"


        import pyre.inventory as pyre

        mode         = pyre.str("mode", default="Verbose")
        colorScheme  = pyre.str("color-scheme", default="Linux")
        callPdb      = pyre.bool("call-pdb", default=False)

        callPdb.meta['tip'] = 'call pdb when an exception occurs'


        def __init__(self):
            Component.__init__(self)
            self.excepthook = None


        def _init(self):
            import sys

            if sys.stderr.isatty():
                colorScheme = self.colorScheme
            else:
                colorScheme = "NoColor"

            if sys.stdin.isatty() and sys.stdout.isatty() and sys.stderr.isatty():
                callPdb = self.callPdb
            else:
                callPdb = False

            self.excepthook = IPython.ultraTB.FormattedTB(
                mode          = self.mode,
                color_scheme  = colorScheme,
                call_pdb      = callPdb
                )

            return


    hook = ultraTB()

    return hook


# end of file 
