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


from .Device import Device


class File(Device):

    class Inventory(Device.Inventory):

        import pythia.pyre.inventory

        name = pythia.pyre.inventory.str("name", default="journal.log")
        name.meta['tip'] = "the name of the file in which messages will be placed"

    def createDevice(self):
        logfile = open(self.inventory.name, "a")

        import os
        import time

        logfile.write(" ** MARK: opened by %s on %s\n" % (os.getpid(), time.ctime()))

        from pythia.journal.devices.File import File
        return File(logfile)

    def __init__(self):
        Device.__init__(self, "file")
        return


# version
__id__ = "$Id: File.py,v 1.2 2005/03/10 06:16:37 aivazis Exp $"

# End of file
