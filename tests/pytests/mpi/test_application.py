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

from .MPIApp import MPIApp


class TestApplication(unittest.TestCase):

    def test_constructor(self):
        app = MPIApp()
        self.assertEqual("mpiapp", app.name)

    def test_run(self):
        app = MPIApp()
        app.nodes = 3
        app.run(argv=["mpiapp", "--launcher.command=mpiexec -n ${nodes} -host localhost:${nodes}"])
        for node in range(app.nodes):
            filename = app.log_filename(node)
            with open(filename, "r") as fin:
                linesE = app.log_output(node)
                lines = fin.readlines()
                self.assertEqual(len(linesE), len(lines), msg="Mismatch for process {}".format(node))
                for lineE, line in zip(linesE, lines):
                    self.assertEqual(lineE, line, msg="Mismatch for process {}".format(node))
            os.remove(filename)


def load_tests(loader, tests, pattern):
    TEST_CLASSES = [TestApplication]

    suite = unittest.TestSuite()
    for cls in TEST_CLASSES:
        suite.addTests(loader.loadTestsFromTestCase(cls))
    return suite


if __name__ == "__main__":
    unittest.main(verbosity=2)


# End of file
