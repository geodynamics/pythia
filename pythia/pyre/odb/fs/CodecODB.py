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


from pythia.pyre.odb.common.Codec import Codec


class CodecODB(Codec):

    def open(self, db, mode='r'):
        """open the file <db> in mode <mode> and place its contents in a shelf"""

        filename = self.resolve(db)

        import os
        exists = os.path.isfile(filename)

        if mode in ['r'] and not exists:
            raise IOError("file not found: '%s'" % filename)

        shelf = self._shelf(filename, False)
        self._decode(shelf)

        if mode == 'r':
            shelf._const = True
        else:
            shelf._const = False

        return shelf

    def resolve(self, db):
        return db + '.' + self.extension

    def __init__(self, encoding, extension=None):
        if extension is None:
            extension = encoding

        Codec.__init__(self, encoding, extension)

        # public data
        self.renderer = self._createRenderer()

        return

    def _shelf(self, filename, const):
        """create a shelf for the contents of the db file"""

        from .Shelf import Shelf
        return Shelf(filename, const, self)

    def _decode(self, shelf):
        """lock and then read the contents of the file into the shelf"""

        stream = open(shelf.name, "r")
        exec(stream.read(), shelf)

        return

    def _createRenderer(self):
        """create a weaver for storing shelves"""

        from pythia.pyre.weaver.Weaver import Weaver
        weaver = Weaver()
        return weaver


# version
__id__ = "$Id: CodecODB.py,v 1.1.1.1 2005/03/08 16:13:41 aivazis Exp $"

# End of file
