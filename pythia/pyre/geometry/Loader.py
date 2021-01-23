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


from .GeometricalModeller import GeometricalModeller


class Loader(GeometricalModeller):

    class Inventory(GeometricalModeller.Inventory):

        import pythia.pyre.inventory

        source = pythia.pyre.inventory.str("source", default="sample.pml")

    def model(self):
        import os

        source = self.source

        base, ext = os.path.splitext(self.source)
        if not ext:
            source += ".pml"
            format = "pml"
        else:
            format = ext[1:]

        stream = open(source, "r")

        return self.retrieveModel(stream, format)

    def __init__(self, name=None):
        GeometricalModeller.__init__(self, name)

        self.source = None

        return

    def _config(self):
        self.source = self.inventory.source
        return


# version
__id__ = "$Id: Loader.py,v 1.1.1.1 2005/03/08 16:13:44 aivazis Exp $"

# End of file
