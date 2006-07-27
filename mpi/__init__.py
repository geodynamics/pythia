#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

# timers
def timingCenter():
    from TimingCenter import timingCenter
    return timingCenter()


def timer(name):
    return timingCenter().timer(name)


def world():
    try:
        import _mpi
    except:
        from DummyCommunicator import DummyCommunicator
        return DummyCommunicator()
    else:
        import Communicator
        return Communicator.world()


def inParallel():
    try:
        import _mpi
    except:
        return 0
    else:
        return 1


def processors():
    try:
        import _mpi
    except:
        return 1
    else:
        return world().size
    

def copyright():
    return "pythia.mpi: Copyright (c) 1998-2005 Michael A.G. Aivazis"


# version
__version__ = "0.8"
__id__ = "$Id: __init__.py,v 1.1.1.1 2005/03/08 16:13:30 aivazis Exp $"

# End of file
