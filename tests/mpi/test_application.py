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
import os

from MPIApp import MPIApp


class TestApplication(unittest.TestCase):

    def test_constructor(self):
        app = MPIApp()
        self.assertEqual("mpiapp", app.name)
        
    def test_run(self):
        app = MPIApp()
        app.nodes = 3
        app.run(argv=["mpiapp"])
        for node in range(app.nodes):
            filename = app.log_filename(node)
            with open(filename, "r") as fin:
                linesE = app.log_output(node)
                lines = fin.readlines()
                self.assertEqual(len(linesE), len(lines), msg="Mismatch for process {}".format(node))
                for lineE, line in zip(linesE, lines):
                    self.assertEqual(lineE, line, msg="Mismatch for process {}".format(node))
            os.remove(filename)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestApplication))
    unittest.TextTestRunner(verbosity=2).run(suite)

        
# End of file
