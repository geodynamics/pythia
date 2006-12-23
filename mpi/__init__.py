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


from _mpi import *
from Application import Application


def world():
    import Communicator
    return Communicator.world()


def mpistart(argv=None, **kwds):
    """entry point for MPI applications"""

    import sys
    from pyre.applications import start, AppRunner

    kwds = kwds.get('kwds', dict())
    kwds['message'] = 'onComputeNodes'

    try:
        start(argv,
              applicationClass = AppRunner,
              kwds = kwds)
    except:
        #MPI_Abort(MPI_COMM_WORLD, 1)
        raise
    
    return 0


# end of file
