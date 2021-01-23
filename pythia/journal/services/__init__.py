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


def daemon(name=None):
    from .Daemon import Daemon
    return Daemon(name)


def service(name=None):
    from .JournalService import JournalService
    return JournalService(name)


def evaluator(name=None):
    from .Evaluator import Evaluator
    return Evaluator(name)


def pickler(name=None):
    if name is None:
        name = "journal-pickler"

    from .Pickler import Pickler
    return Pickler(name)


def request(command, args=None):
    from .ServiceRequest import ServiceRequest
    return ServiceRequest(command, args)


# End of file
