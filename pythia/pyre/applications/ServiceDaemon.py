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


from .Application import Application
from .Daemon import Daemon as Stager
from .ComponentHarness import ComponentHarness


class ServiceDaemon(ComponentHarness, Application, Stager):

    class Inventory(Application.Inventory):

        import pythia.pyre.inventory

        client = pythia.pyre.inventory.str('client')
        home = pythia.pyre.inventory.str('home', default='/tmp')

    def main(self, *args, **kwds):
        # harness the service
        idd = self.harnessComponent()
        if not idd:
            return

        # generate client configuration
        self.generateClientConfiguration(idd)

        # enter the indefinite loop waiting for requests
        idd.serve()

        return

    def generateClientConfiguration(self, component):
        clientName = self.inventory.client
        if not clientName:
            clientName = component.name + '-session'

        registry = self.createRegistry()
        componentRegistry = registry.getNode(clientName)
        component.generateClientConfiguration(componentRegistry)

        with open(clientName + ".pml", "w") as stream:
            document = self.weaver.render(registry)
            stream.write("\n".join(document))
            stream.write("\n")

        return

    def __init__(self, name):
        Application.__init__(self, name, facility='daemon')
        Stager.__init__(self)
        ComponentHarness.__init__(self)
        return

    def _configure(self):
        Application._configure(self)

        import os
        self.home = os.path.abspath(self.inventory.home)
        return


# version
__id__ = "$Id: ServiceDaemon.py,v 1.1 2005/03/11 06:58:29 aivazis Exp $"

# End of file
