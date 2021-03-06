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



from pythia.pyre.inventory.odb.Registry import Registry
from pythia.pyre.odb.fs.CodecODB import CodecODB
from .Parser import Parser
from os.path import split, splitext


class CodecConfig(CodecODB):

    def __init__(self):
        CodecODB.__init__(self, encoding='cfg')
        return

    def _createRenderer(self):
        from .Renderer import Renderer
        return Renderer()

    def _decode(self, shelf):
        root = Registry("root")
        td, fn = split(shelf.name)
        if not td: td = "."
        basename = splitext(fn)[0]
        macros = { 'td': td, 'basename': basename }
        parser = Parser(root, macros=macros)
        try:
            parser.read(shelf.name)
        except (AttributeError, KeyError) as err:
            raise AttributeError("Error parsing '{fp.name}' line {fp.lineno}".format(fp=parser._sections.fp))
        shelf['inventory'] = root
        shelf._frozen = True
        return


# end of file
