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


from pythia.pyre.services.TCPService import TCPService


class IDDService(TCPService):

    class Inventory(TCPService.Inventory):

        import pythia.pyre.idd
        import pythia.pyre.inventory

        tid = pythia.pyre.inventory.int('tid')
        date = pythia.pyre.inventory.str('date')

        configfile = pythia.pyre.inventory.str("config", default=None)

        marshaller = pythia.pyre.inventory.facility("marshaller", factory=pythia.pyre.idd.pickler)
        locator = pythia.pyre.inventory.facility("recordLocator", factory=pythia.pyre.idd.recordLocator)

    def generateClientConfiguration(self, registry):
        """update the given registry node with sufficient information to grant access to clients"""

        import pythia.pyre.parsing.locators
        locator = pythia.pyre.parsing.locators.simple('service')

        # get the inherited settings
        TCPService.generateClientConfiguration(self, registry)

        # record the marshaller name
        registry.setProperty('marshaller', self.marshaller.name, locator)

        # get the marshaller to record his configuration
        marshaller = registry.getNode(self.marshaller.name)
        self.marshaller.generateClientConfiguration(marshaller)

        return

    def token(self):
        if self._reload:
            self.initialize()

        from .Token import Token
        token = Token()

        token.tid = self.tid
        token.date = self.date
        token.locator = self.locator.encode(self.tid, self.date)

        self._info.log("issued token: %s" % token)
        self.tid += 1

        return token

    def onTimeout(self, *unused):
        self._info.log("thump")
        self.verify()
        return True

    def onReload(self, *unused):
        self._reload = True
        return

    def initialize(self, *unused):
        self._debug.log("reading '%s' state from %r" % (self.name, self.configfile))
        self._loadGeneratorParameters()

        # check that the loaded configuration is ok
        self.verify()

        self._reload = False

        return

    def verify(self):
        import time
        tick = time.localtime()

        date = time.strftime("%y%m%d", tick)

        self._debug.log("checking whether date=%s is current" % self.date)
        if date != self.date:
            self.date = date
            self.tid = 0

            self._debug.log("resetting: tid=%d, date=%s" % (self.tid, self.date))

            self._storeGeneratorParameters()

        return

    def __init__(self, name=None):
        if name is None:
            name = 'idd'
        TCPService.__init__(self, name)

        self.tid = 0
        self.date = ""

        # the filename that holds the persistent copy of the locator generators
        self.configfile = self.name + '-config.pml'

        # the codec for record locators
        self.locator = None

        # private data
        self._reload = True

        return

    def _configure(self):
        TCPService._configure(self)

        self.tid = self.inventory.tid
        self.date = self.inventory.date
        self.locator = self.inventory.locator
        self.marshaller = self.inventory.marshaller

        if self.inventory.configfile is not None:
            self.configfile = self.inventory.configfile

        return

    def _init(self):
        TCPService._init(self)

        # register the routine that stores counter when we exit
        import atexit
        atexit.register(self._storeGeneratorParameters)

        # prime the counter
        self.initialize()

        return

    def _loadGeneratorParameters(self):
        import os
        base, ext = os.path.splitext(self.configfile)

        try:
            registry = self.loadConfiguration(base)
        except IOError:
            return

        # extract my settings
        mine = registry.getNode(self.name)

        # apply them
        self.updateConfiguration(mine)
        self.applyConfiguration()

        return

    def _storeGeneratorParameters(self):
        self._debug.log("saving '%s' configuration in %r" % (self.name, self.configfile))
        registry = self._describe()

        if registry:
            stream = open(self.configfile, "w")
            text = self.weaver.weave(registry, stream)
            stream.close()

        return

    def _describe(self):
        import pythia.pyre.inventory
        registry = pythia.pyre.inventory.registry('root')

        mine = registry.getNode(self.name)
        mine.setProperty("tid", self.tid, None)
        mine.setProperty("date", self.date, None)

        # get the marshaller to save himself
        self.marshaller.retrieveConfiguration(mine)

        return registry


# version
__id__ = "$Id: IDDService.py,v 1.7 2005/04/28 03:50:06 pythia.pyre Exp $"

# End of file
