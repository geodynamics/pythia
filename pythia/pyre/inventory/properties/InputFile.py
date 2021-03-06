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


from pythia.pyre.inventory.Property import Property
import sys


class InputFile(Property):

    def __init__(self, name, default=sys.stdin, meta=None, validator=None):
        Property.__init__(self, name, "file", default, meta, validator)
        return

    def _cast(self, value):
        if isinstance(value, str):
            if value == "stdin":
                import sys
                value = sys.stdin
            else:
                value = open(value, "r")

        return value


# version
__id__ = "$Id: InputFile.py,v 1.2 2005/03/11 06:09:32 aivazis Exp $"

# End of file
