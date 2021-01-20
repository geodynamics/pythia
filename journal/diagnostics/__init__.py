#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def firewall(name):
    from .Firewall import Firewall
    return Firewall().diagnostic(name)


def debug(name):
    from .Debug import Debug
    return Debug().diagnostic(name)


def info(name):
    from .Info import Info
    return Info().diagnostic(name)


def warning(name):
    from .Warning import Warning
    return Warning().diagnostic(name)


def error(name):
    from .Error import Error
    return Error().diagnostic(name)


# End of file
