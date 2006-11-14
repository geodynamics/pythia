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


from pyre.components.Component import Component
from Executive import Executive


class Application(Component, Executive):


    name = "application"


    class Inventory(Component.Inventory):

        import pyre.inventory

        typos = pyre.inventory.str(
            name='typos', default='strict',
            validator=pyre.inventory.choice(['relaxed', 'strict', 'pedantic']))
        typos.meta['tip'] = 'specifies the handling of typos in the names of properties and facilities'

        import pyre.weaver
        weaver = pyre.inventory.facility("weaver", factory=pyre.weaver.weaver)
        weaver.meta['tip'] = 'the pretty printer of my configuration as an XML document'

        import journal
        journal = journal.facility()
        journal.meta['tip'] = 'the logging facility'


    def run(self, *args, **kwds):

        # build storage for the user input
        registry = self.createRegistry()
        self.registry = registry

        # command line
        argv = self.getArgv(*args, **kwds)
        commandLine = self.processCommandline(registry, argv)
        action = commandLine.action
        self.argv = commandLine.processed
        self.unprocessedArguments = commandLine.unprocessed

        # curator
        curator = self.createCurator()
        self.initializeCurator(curator, registry)

        # look for my settings
        self.initializeConfiguration()

        # read parameter files given on the command line
        self.readParameterFiles(registry)

        # give descendants an opportunity to collect input from other (unregistered) sources
        self.collectUserInput(registry)

        # update user options from the command line
        self.updateConfiguration(registry)

        # transfer user input to my inventory
        context = self.applyConfiguration()

        # verify that the user input did not contain any typos
        if not self.verifyConfiguration(context, self.inventory.typos):
            import sys
            sys.exit("%s: configuration error(s)" % self.name)

        # initialize the trait cascade
        self.init()

        # print a startup page
        self.generateBanner()

        # the main application behavior
        action = action and getattr(self, action)
        if action:
            action()
        elif self._showHelpOnly:
            pass
        else:
            message = kwds.get('message', 'execute')
            method = getattr(self, message)
            method(*args, **kwds)

        # shutdown
        self.fini()

        return


    def initializeCurator(self, curator, registry):
        if registry is not None:
            curator.config(registry)
            
        # install the curator
        self.setCurator(curator)

        # adjust the depositories
        # first, register the application specific depository
        curator.depositories += self.inventory.getDepositories()
        # then, any extras specified by my descendants
        curator.addDepositories(*self._getPrivateDepositoryLocations())

        return curator


    def readParameterFiles(self, registry):
        """read parameter files given on the command line"""
        import journal
        error = journal.error(self.name)
        from os.path import isfile, splitext
        argv = self.argv
        self.argv = []
        for arg in argv:
            base, ext = splitext(arg)
            encoding = ext[1:] # NYI: not quite
            codec = self.getCurator().codecs.get(encoding)
            if codec:
                try:
                    shelf = codec.open(base)
                except Exception, e:
                    error.log(str(e))
                else:
                    paramRegistry = shelf['inventory'].getFacility(self.name)
                    if paramRegistry:
                        self.updateConfiguration(paramRegistry)
            else:
                self.argv.append(arg)
        return

    
    def collectUserInput(self, registry):
        """collect user input from additional sources"""
        return


    def generateBanner(self):
        """print a startup screen"""
        return


    def entryName(self):
        return self.__class__.__module__ + ':' + self.__class__.__name__


    def workingSet(self):
        """Return the minimal working set for this application."""
        
        from pkg_resources import WorkingSet, Environment, parse_requirements
        
        requires = self.requires()
        workingSet = WorkingSet([])
        requirements = parse_requirements(requires)
        
        for dist in workingSet.resolve(requirements, Environment()):
            workingSet.add(dist)

        return workingSet


    def path(self):
        """Return the minimal Python search path for this application."""
        workingSet = self.workingSet()
        return workingSet.entries


    def pathString(self):
        return ':'.join(self.path())


    def __init__(self, name=None, facility=None):
        Component.__init__(self, name, facility)
        Executive.__init__(self)
    
        # my name as seen by the shell
        import sys
        self.filename = sys.argv[0]

        # commandline arguments left over after parsing
        self.argv = []
        self.unprocessedArguments = []

        # the user input
        self.registry = None

        # the code generator
        self.weaver = None

        return


    def _init(self):
        Component._init(self)
        self.weaver = self.inventory.weaver

        renderer = self.getCurator().codecs['pml'].renderer
        self.weaver.renderer = renderer

        return


    def _getPrivateDepositoryLocations(self):
        return []


    def dumpDefaults(self):
        configuration = self.collectDefaults()
        # save the configuation as a PML file
        configPml = self.name + "-defaults.pml"
        pml = open(configPml, 'w')
        print >> pml, "\n".join(self.weaver.render(configuration))
        pml.close()



# version
__id__ = "$Id: Application.py,v 1.6 2005/04/05 21:34:12 aivazis Exp $"

# End of file 
