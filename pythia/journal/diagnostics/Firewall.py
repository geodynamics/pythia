#!/usr/bin/env python
#
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
#  <LicenseText>
#
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from .Index import Index


class Firewall(Index):

    def init(self):
        Index.init(self, "firewall", defaultState=True, fatal=True)
        return

    def _proxyState(self, name):
        from .ProxyState import ProxyState
        import pythia.journal
        return ProxyState(pythia.journal._journal.firewall(name))


# version
__id__ = "$Id: Firewall.py,v 1.1.1.1 2005/03/08 16:13:53 aivazis Exp $"

#  End of file
