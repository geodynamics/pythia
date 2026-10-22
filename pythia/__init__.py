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


from importlib.metadata import version as _get_version, PackageNotFoundError
try:
    version = _get_version("pythia")
except PackageNotFoundError:
    version = "Could not get version information via importlib.metadata."

__version__ = version


def copyright():
    return "journal: Copyright (c) 1998-2005 Michael A.G. Aivazis"


# End of file 
