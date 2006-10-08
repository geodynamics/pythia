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


# misc
def copyright():
    return "pyre: Copyright (c) 1998-2005 Michael A.G. Aivazis"


# version
__version__ = "0.8"
__id__ = "$Id: __init__.py,v 1.1.1.1 2005/03/08 16:13:40 aivazis Exp $"



# a component which allows the user to configure the Python system
# itself using Pyre


from pyre.components import Component


class System(Component):


    name = "sys"


    import pyre.hooks
    excepthook = pyre.hooks.facility("excepthook", family="excepthook", default="ultraTB")


    def startup(self):
        import pyre.inventory
        registry = self.createRegistry()
        self.registry = registry
        curator = pyre.inventory.curator(self.name)
        curator.config(registry)
        self.setCurator(curator)
        curator.depositories += self.inventory.getDepositories()
        self.initializeConfiguration()
        self.applyConfiguration()
        self.init()

        import sys
        if self.excepthook:
            sys.excepthook = self.excepthook.excepthook

        return


system = System()
system.startup()


# End of file 
