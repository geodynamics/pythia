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


try:
    from pkg_resources import get_distribution
    version = get_distribution("pythia").version
except:
    version = "Could not get verion information via pkg_resources."

__version__ = version


def copyright():
    return "journal: Copyright (c) 1998-2005 Michael A.G. Aivazis"


# End of file 
