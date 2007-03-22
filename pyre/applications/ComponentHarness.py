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


class ComponentHarness(object):


    def harnessComponent(self):
        """harness an external component"""

        # create the component
        component = self.createComponent()

        # initialize the persistent store used by the component to configure itself
        curator = self.prepareComponentCurator()

        # prepare optional configuration for the component
        registry = self.prepareComponentConfiguration(component)

        # configure the component
        # collect unknown traits for the components and its subcomponents
        context = self.configureHarnessedComponent(component, curator, registry)

        if not context.verifyConfiguration(component, 'strict'):
            return

        # initialize the component
        component.init()

        # register it
        self.component = component

        return component


    def createComponent(self):
        """create the harnessed component"""
        raise NotImplementedError(
            "class %r must override 'createComponent'" % self.__class__.__name__)


    def configureHarnessedComponent(self, component, curator, registry):
        """configure the harnessed component"""

        # link the component with the curator
        component.setCurator(curator)
        component.initializeConfiguration()

        # update the component's inventory with the optional settings we
        # have gathered on its behalf
        component.updateConfiguration(registry)

        # load the configuration onto the inventory
        context = component.applyConfiguration()

        return context


    def __init__(self):
        self.component = None
        return


# version
__id__ = "$Id: ComponentHarness.py,v 1.2 2005/03/11 07:00:17 aivazis Exp $"

# End of file 
