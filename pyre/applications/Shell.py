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


from pyre.inventory.Configurable import Configurable


try:
    import IPython.ultraTB
    defaultExceptHook = "ultraTB"
except ImportError:
    defaultExceptHook = "current"


class Shell(Configurable):


    import pyre.inventory
    version = pyre.inventory.bool("version")
    
    import pyre.hooks
    excepthook = pyre.hooks.facility("excepthook", family="excepthook",
                                     default=defaultExceptHook)

    import journal
    journal = journal.facility()
    journal.meta['tip'] = 'the logging facility'


    def __init__(self, app):
        Configurable.__init__(self, app.name)

        self.app = app
        self.registry = None


    def run(self, *args, **kwds):

        app = self.app

        # build storage for the user input
        registry = app.createRegistry()

        # command line
        argv = app.getArgv(*args, **kwds)
        commandLine = app.processCommandline(registry, argv)
        action = commandLine.action
        app.argv = commandLine.processed
        app.unprocessedArguments = commandLine.unprocessed

        # curator
        curator = app.createCurator()
        app.initializeCurator(curator, registry)
        self.setCurator(curator)

        # config context
        context = app.newConfigContext()

        # look for settings
        self.initializeConfiguration()
        self.inventory._priv_registry, app.inventory._priv_registry = self.filterConfiguration(self.inventory._priv_registry)

        # read parameter files given on the command line
        app.readParameterFiles(registry, context)

        # give descendants an opportunity to collect input from other (unregistered) sources
        app.collectUserInput(registry, context)

        # split the configuration in two
        registry, app.registry = self.filterConfiguration(registry)
        self.registry = registry

        # update user options from the command line
        self.updateConfiguration(registry)

        # transfer user input to my inventory
        self.applyConfiguration(context)

        # verify that my input did not contain any typos
        if not context.verifyConfiguration('strict'):
            import sys
            sys.exit("%s: configuration error(s)" % self.name)

        # initialize the trait cascade
        self.init()

        import sys
        if self.excepthook:
            sys.excepthook = self.excepthook.excepthook

        # initialize the application
        app.updateConfiguration(app.registry)
        app.applyConfiguration(context)

        # verify that the application input did not contain any typos
        if not app.verifyConfiguration(context, app.inventory.typos):
            app.usage()
            import sys
            sys.exit("%s: configuration error(s)" % app.name)

        app.init()

        # print a startup page
        app.generateBanner()

        # the main application behavior
        action = action and getattr(app, action)
        if action:
            action()
        elif self.version:
            app.version()
        elif app._helpRequested:
            app.help()
        else:
            message = kwds.get('message', 'execute')
            method = getattr(app, message)
            method(*args, **kwds)

        # shutdown
        app.fini()
        self.fini()

        return


# end of file
