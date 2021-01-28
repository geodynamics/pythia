# ======================================================================
#
# Brad T. Aagaard, U.S. Geological Survey
#
# This code was developed as part of the Computational Infrastructure
# for Geodynamics (http://geodynamics.org).
#
# Copyright (c) 2010-2017 University of California, Davis
#
# See COPYING for license information.
#
# ======================================================================
#

import unittest


from pythia.mpi.Application import Application
import pythia.mpi.Communicator


class MPICommApp(Application, unittest.TestCase):

    def __init__(self, name="mpicommapp"):
        Application.__init__(self, name)
        self.world = None
        self.nodes = 2

    def main(self, *args, **kwds):
        self.world = pythia.mpi.Communicator.world()

        self.test_world()
        self.test_barrier()
        self.test_group()
        self.test_port()
        
    def test_world(self):
        self.assertTrue(pythia.mpi.MPI_COMM_WORLD == self.world.handle())
        
    def test_barrier(self):
        self.world.barrier()

    def test_group(self):
        group = self.world.group()
        self.assertTrue(self.world.size == group.size)

    def test_port(self):
        TAG = 123

        if self.world.rank == 0:
            port = self.world.port(1, TAG)
        elif self.world.rank == 1:
            port = self.world.port(0, TAG)
        
        
# End of file
