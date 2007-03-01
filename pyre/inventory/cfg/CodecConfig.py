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


from pyre.inventory.odb.Registry import Registry
from pyre.odb.fs.CodecODB import CodecODB
from Parser import Parser


class CodecConfig(CodecODB):

    def __init__(self):
        CodecODB.__init__(self, encoding='cfg')
        return

    def _createRenderer(self):
        from Renderer import Renderer
        return Renderer()

    def _decode(self, shelf):
        root = Registry("root")
        parser = Parser(root)
        parser.read(shelf.name)
        shelf['inventory'] = root
        shelf._frozen = True
        return


# end of file
