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


class Bool(Property):


    def __init__(self, name, default=False, meta=None, validator=None):
        Property.__init__(self, name, "bool", default, meta, validator)
        return


    def _cast(self, value):
        if isinstance(value, str):
            import pythia.pyre.util.bool
            return pythia.pyre.util.bool.bool(value)

        return bool(value)
    

# version
__id__ = "$Id: Bool.py,v 1.1.1.1 2005/03/08 16:13:44 aivazis Exp $"

# End of file 
