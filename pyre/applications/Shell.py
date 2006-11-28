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


from pyre.components import Component


class Shell(Component):


    name = "shell"


    import pyre.hooks
    excepthook = pyre.hooks.facility("excepthook", family="excepthook", default="ultraTB")

    import journal
    journal = journal.facility()
    journal.meta['tip'] = 'the logging facility'


    def runApplication(self, ApplicationClass, **kwds):
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

        app = ApplicationClass()
        app.run(**kwds)

        return


# end of file
