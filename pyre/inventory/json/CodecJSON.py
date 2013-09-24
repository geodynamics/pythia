#!/usr/bin/env python
#
# ----------------------------------------------------------------------
#
# Brad T. Aagaard, U.S. Geological Survey
#
# This code was developed as part of the Computational Infrastructure
# for Geodynamics (http://geodynamics.org).
#
# Copyright (c) 2010-2013 University of California, Davis
#
# ----------------------------------------------------------------------

from pyre.odb.fs.CodecODB import CodecODB
from Parser import Parser


class CodecJSON(CodecODB):

    def __init__(self):
        CodecODB.__init__(self, encoding='json')
        return


    def _createRenderer(self):
        from Renderer import Renderer
        return Renderer()


    def _decode(self, shelf):
        parser = Parser(shelf.name)
        root = parser.read()
        shelf['inventory'] = root
        shelf._frozen = True
        return


# end of file
