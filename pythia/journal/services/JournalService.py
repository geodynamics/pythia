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


class JournalService(TCPService):

    class Inventory(TCPService.Inventory):

        import pythia.pyre.inventory

        import pythia.journal.services
        marshaller = pythia.pyre.inventory.facility("marshaller", factory=pythia.journal.services.pickler)

    def record(self, entry):
        import pythia.journal
        pythia.journal.journal().record(entry)
        return

    def generateClientConfiguration(self, registry):
        import pythia.pyre.parsing.locators
        locator = pythia.pyre.parsing.locators.simple('service')

        # get the inheriter settings
        TCPService.generateClientConfiguration(self, registry)

        # record the marshaller key
        # FIXME: generalize this to other picklers, like idd and ipa
        self.marshaller.generateClientConfiguration(registry)

        return

    def __init__(self, name=None):
        if name is None:
            name = 'journald'

        TCPService.__init__(self, name)

        # the remote request marshaller
        self.marshaller = None
        self._counter = 0

        return

    def _configure(self):
        TCPService._configure(self)
        self.marshaller = self.inventory.marshaller
        return


# version
__id__ = "$Id: JournalService.py,v 1.3 2005/03/14 07:28:47 aivazis Exp $"

# End of file
