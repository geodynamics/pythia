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


class Mesh(object):

    def handle(self):
        return self._mesh

    def statistics(self):
        import pythia.pyre._pyre
        return pythia.pyre._pyre.statistics(self._mesh)

    def vertex(self, vertexid):
        import pythia.pyre._pyre
        return pythia.pyre._pyre.vertex(self._mesh, vertexid)

    def simplex(self, simplexid):
        import pythia.pyre._pyre
        return pythia.pyre._pyre.simplex(self._mesh, simplexid)

    def vertices(self):
        import pythia.pyre._pyre
        dim, order, vertices, simplices = pythia.pyre._pyre.statistics(self._mesh)

        for i in range(vertices):
            yield pythia.pyre._pyre.vertex(self._mesh, i)

        return

    def simplices(self):
        import pythia.pyre._pyre
        dim, order, vertices, simplices = pythia.pyre._pyre.statistics(self._mesh)

        for i in range(simplices):
            yield pythia.pyre._pyre.simplex(self._mesh, i)

        return

    def __init__(self, dim, order):
        self.dim = dim
        self.order = order

        try:
            import pythia.pyre._pyre
        except ImportError:
            import pythia.journal.diagnostics
            error = pythia.journal.diagnostics.error('pyre')
            error.line("unable to import the C++ pythia.pyre extensions")
            error.log("mesh objects are not supported")
            self._mesh = None
            return

        self._mesh = pythia.pyre._pyre.createMesh(dim, order)

        return


# version
__id__ = "$Id: Mesh.py,v 1.1.1.1 2005/03/08 16:13:44 aivazis Exp $"

# End of file
