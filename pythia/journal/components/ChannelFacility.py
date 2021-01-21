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


from pythia.pyre.inventory.Facility import Facility


class ChannelFacility(Facility):


    def __init__(self, name):
        from .Channel import Channel
        Facility.__init__(self, name=name, factory=Channel, args=[name])

        return


    def _retrieveComponent(self, instance, componentName):
        from .Channel import Channel
        channel = Channel(componentName)

        import pythia.pyre.parsing.locators
        locator = pythia.pyre.parsing.locators.builtIn()

        return channel, locator
    

# version
__id__ = "$Id: ChannelFacility.py,v 1.1.1.1 2005/03/08 16:13:53 aivazis Exp $"

# End of file 
