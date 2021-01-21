#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                               Michael A.G. Aivazis
#                        (C) 1998-2005 All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 


from .Load import Load


class Bath(Load):


    class Inventory(Load.Inventory):

        import pythia.pyre.inventory
        
        from pythia.pyre.units.mass import kg
        from pythia.pyre.units.length import meter
        from pythia.pyre.units.volume import liter
        from pythia.pyre.units.pressure import atm

        ambient = pythia.pyre.inventory.dimensional("ambient", default=1.0*atm)
        surface = pythia.pyre.inventory.dimensional("surface", default=0.0*meter)
        density = pythia.pyre.inventory.dimensional("density", default=1.0*kg/liter)


    def updatePressure(self, boundary):

        ambient = self.ambient.value
        surface = self.surface.value
        density = self.density.value

        import pulse
        pulse.bath(boundary.mesh.handle(), boundary.pressure, ambient, surface, density)

        return


    def advance(self, dt):
        return
    

    def __init__(self):
        Load.__init__(self, "bath")
        self.ambient = None
        self.surface = None
        self.density = None
        return


    def _configure(self):
        self.ambient = self.inventory.ambient
        self.surface = self.inventory.surface
        self.density = self.inventory.density
        return


# version
__id__ = "$Id: Bath.py,v 1.1.1.1 2005/03/08 16:13:57 aivazis Exp $"

#  End of file 
