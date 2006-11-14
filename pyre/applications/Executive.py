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


class Executive(object):


    # factories
    def createCommandlineParser(self):
        """create a command line parser"""
        
        import pyre.applications
        return pyre.applications.commandlineParser()


    def createRegistry(self, name=None):
        """create a registry instance to store my configuration"""

        if name is None:
            name = self.name

        import pyre.inventory
        return pyre.inventory.registry(name)


    def createCurator(self, name=None):
        """create a curator to handle the persistent store"""

        if name is None:
            name = self.name

        import pyre.inventory
        curator = pyre.inventory.curator(name)

        return curator


    # configuration
    def getArgv(self, *args, **kwds):
        argv = kwds.get('argv')
        if argv is None:
            import sys
            argv = sys.argv
        self.arg0 = argv[0]
        self._requires = kwds.get('requires')
        argv = argv[1:]
        return argv


    def requires(self):
        if self._requires is None:
            from __main__ import __requires__
            self._requires = __requires__
        return self._requires


    def processCommandline(self, registry, argv=None, parser=None):
        """convert the command line arguments to a trait registry"""

        if parser is None:
            parser = self.createCommandlineParser()

        parser.parse(registry, argv)

        return parser


    def verifyConfiguration(self, context, mode='strict'):
        """verify that the user input did not contain any typos"""

        return context.verifyConfiguration(mode)


    def pruneRegistry(self):
        registry = self.registry
        
        for trait in self.inventory.properties():
            name = trait.name
            registry.deleteProperty(name)

        for trait in self.inventory.components():
            for name in trait.aliases:
                registry.extractNode(name)

        return registry


    # the default application action
    def main(self, *args, **kwds):
        return


    # user assistance
    def help(self):
        print 'Please consider writing a help screen for this application'
        return


    def complete(self):
        # NYI: bash tab-completion
        return


    def usage(self):
        print 'Please consider writing a usage screen for this application'
        return


    def __init__(self):
        self.arg0 = self.name
        self._requires = None


# version
__id__ = "$Id: Executive.py,v 1.1.1.1 2005/03/08 16:13:48 aivazis Exp $"

# End of file 
