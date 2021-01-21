#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from pythia.pyre.components.Component import Component


class Channel(Component):

    def updateConfiguration(self, registry):
        from pythia.pyre.util.bool import bool
        listing = self._listing(registry)

        from pythia.journal import journal
        for category, state in listing:
            journal().channel(self.name).diagnostic(category).state = bool(state)

        return []

    def __init__(self, name):
        Component.__init__(self, name, name)
        return

    def _listing(self, registry):
        listing = [
            (name, descriptor.value) for name, descriptor in registry.properties.items()
        ]

        listing += [
            ("%s.%s" % (nodename, name), value)
            for nodename, node in registry.facilities.items()
            for name, value in self._listing(node)
        ]

        return listing


# version
__id__ = "$Id: Channel.py,v 1.1.1.1 2005/03/08 16:13:53 aivazis Exp $"

# End of file
