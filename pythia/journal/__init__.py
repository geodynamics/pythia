#!/usr/bin/env python
#
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
#  <LicenseText>
#
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def journal():
    global _theJournal
    if _theJournal is not None:
        return _theJournal

    from .Journal import Journal
    _theJournal = Journal("journal")
    return _theJournal


# register known severities
def register():
    from .diagnostics.Firewall import Firewall
    from .diagnostics.Debug import Debug
    from .diagnostics.Info import Info
    from .diagnostics.Warning import Warning
    from .diagnostics.Error import Error

    Firewall()
    Debug()
    Info()
    Warning()
    Error()
    return


# statics
_theJournal = None

# register the known indices
register()

#  End of file
