#!/usr/bin/env python
#
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005 All Rights Reserved
#
#  <LicenseText>
#
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

import pythia.journal.diagnostics
from pythia.pyre.geometry.solids.Body import Body


class Composition(Body):

    _info = pythia.journal.diagnostics.debug("pyre.geometry.operations")


# version
__id__ = "$Id: Composition.py,v 1.1.1.1 2005/03/08 16:13:45 aivazis Exp $"

#
# End of file
