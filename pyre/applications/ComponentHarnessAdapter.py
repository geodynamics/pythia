#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2006  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from ComponentHarness import ComponentHarness


class ComponentHarnessAdapter(ComponentHarness):
    """a mixin class used to create a component harness which is itself a component"""


    def updateConfiguration(self, registry):
        """divide settings between myself and the harnessed component"""
        
        myRegistry, yourRegistry = self.filterConfiguration(registry)
        self.componentRegistry.update(yourRegistry)
        return super(ComponentHarnessAdapter, self).updateConfiguration(myRegistry)


    def _fini(self):
        """finalize the component"""
        
        if self.component:
            self.component.fini()

        return


    def prepareComponentCurator(self):
        """prepare the persistent store manager for the harnessed component"""

        # the host component has a notion of its persistent store that
        # it wants to share with the harnessed component
        return self.getCurator()
        

    def prepareComponentConfiguration(self, component):
        """prepare the settings for the harnessed component"""

        # the host component has a registry with settings for the
        # harnessed component
        registry = self.componentRegistry
        registry.name = component.name

        return registry


    def createComponentRegistry(self):
        """create a registry instance to store a configuration for the harnessed component"""
        
        return self.createRegistry()


    def __init__(self):
        ComponentHarness.__init__(self)
        self.componentRegistry = self.createComponentRegistry()
        return


# end of file 
