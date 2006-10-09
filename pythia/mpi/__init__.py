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


def world():
    import Communicator
    return Communicator.world()


def mpistart(argv=None, **kwds):
    """entry point for MPI applications"""

    import sys
    from pyre.applications import start, AppRunner

    if argv is None:
        argv = sys.argv
    argv = [sys.executable] + argv
    
    MPI_Init(argv)

    argv = argv[1:]

    try:
        start(argv,
              applicationClass = AppRunner,
              kwds = dict(message = 'onComputeNodes'))
    except:
        #MPI_Abort(MPI_COMM_WORLD, 1)
        raise
    
    MPI_Finalize()
    
    return 0


# end of file
