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


from BatchScriptTemplate import BatchScriptTemplate
from Scheduler import Scheduler
from Job import Job


# facilities and components

def scheduler(name, **kwds):
    from pyre.inventory.Facility import Facility
    kwds['vault'] = kwds.get('vault', ['schedulers'])
    kwds['family'] = kwds.get('family', 'scheduler')
    return Facility(name, **kwds)


def job(name, **kwds):
    from pyre.inventory.Facility import Facility
    kwds['factory'] = kwds.get('factory', Job)
    kwds['vault'] = kwds.get('vault', ['schedulers'])
    kwds['family'] = kwds.get('family', 'job')
    return Facility(name, **kwds)


# entry points

def jobstart(argv=None, **kwds):
    """entry point for batch jobs"""

    import sys
    from pyre.applications import start, AppRunner

    return start(argv,
                 applicationClass = AppRunner,
                 kwds = dict(message='onLauncherNode'))


# end of file 
