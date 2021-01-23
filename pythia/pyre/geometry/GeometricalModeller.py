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


from pythia.pyre.components.Component import Component


class GeometricalModeller(Component):


    class Inventory(Component.Inventory):

        import pythia.pyre.weaver
        import pythia.pyre.inventory

        weaver = pythia.pyre.inventory.facility('weaver', factory=pythia.pyre.weaver.weaver)


    def model(self):
        raise NotImplementedError("class '%s' must override 'model'" % self.__class__.__name__)


    def retrieveModel(self, stream, format=None):
        if format is None:
            format = "pml"

        import pythia.pyre.geometry
        parser = pythia.pyre.geometry.parser(format)

        return parser.parse(stream)


    def saveModel(self, bodies, stream, format=None):
        if format is None:
            format = "pml"

        import pythia.pyre.geometry
        self.weaver.renderer = pythia.pyre.geometry.renderer(format)

        document = self.weaver.render(bodies)
        text = "\n".join(document)

        stream.write(text)
        
        return


    def __init__(self, name=None):
        if name is None:
            name = "geometricalModeller"
            
        Component.__init__(self, name, "geometricalModeller")

        self.weaver = None

        return


    def _configure(self):
        self.weaver = self.inventory.weaver
        return


# version
__id__ = "$Id: GeometricalModeller.py,v 1.1.1.1 2005/03/08 16:13:44 aivazis Exp $"

# End of file 
