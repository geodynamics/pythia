#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.components import Component
from pyre.util import expandMacros
from pyre.inventory.odb.Registry import Registry
import os


class Preprocessor(Component):


    def updateConfiguration(self, registry):
        self.macros.update(registry)
        return []


    def expandMacros(self, registry):
        macros = self._prepareMacros()
        self._expandMacros(macros, registry)
        return


    def _prepareMacros(self):
        
        class RecursionProtector(object):
            def __init__(self, macros):
                self.macros = macros
                self.recur = {}
            def __getitem__(self, key):
                if self.recur.has_key(key):
                    return ""
                self.recur[key] = True
                value = expandMacros(self.macros[key], self)
                del self.recur[key]
                return value

        macros = {}
        
        # add environment variables
        macros.update(os.environ)
        
        # flatten my macro registry
        for path, value, locator in self.macros.allProperties():
            key = '.'.join(path[1:])
            macros[key] = value

        return RecursionProtector(macros)


    def _expandMacros(self, macros, registry):
        for name, descriptor in registry.properties.items():
            newValue = expandMacros(descriptor.value, macros)
            descriptor.value = newValue
        for node in registry.facilities.values():
            self._expandMacros(macros, node)
        return


    def __init__(self, name):
        Component.__init__(self, "macros", name)
        self.macros = Registry(self.name)
        return


# end of file
