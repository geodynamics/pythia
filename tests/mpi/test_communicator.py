#!/usr/bin/env nemesis
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

import mpi

from MPICommApp import MPICommApp

class TestCommunicator(unittest.TestCase):
    """This class is just a wrapper class to ensure that the underlying app MPICommApp()
    runs within MPI by way of app running in a subprocess (Pyre's way of running MPI).
    """
    
    def test_communicator(self):
        app = MPICommApp()
        nodes = app.nodes
        app.run(argv=["mpicommapp", "--nodes={:d}".format(nodes)])
        

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestCommunicator))
    unittest.TextTestRunner(verbosity=2).run(suite)

        
# End of file
