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

from pythia.mpi.Launcher import Launcher


class TestLauncher(unittest.TestCase):

    NAME = "mylauncher"

    def test_constructor(self):
        launcher = Launcher(self.NAME)
        self.assertFalse(launcher.dry)

    def test_argv(self):
        NODES = 3
        ARGUMENTS = ["one", "two", "three"]

        launcher = Launcher(self.NAME)
        launcher.nodes = NODES
        launcher.arguments = ARGUMENTS
        argv = launcher.argv()

        argvE = ["mpiexec", "-n", "${nodes}"]
        argvE += [os.path.abspath(os.curdir)]
        argvE += ARGUMENTS
        self.assertEqual(len(argvE), len(argv))
        for argE, arg in zip(argvE, argv):
            self.assertEqual(argE, arg)


def load_tests(loader, tests, pattern):
    TEST_CLASSES = [TestLauncher]

    suite = unittest.TestSuite()
    for cls in TEST_CLASSES:
        suite.addTests(loader.loadTestsFromTestCase(cls))
    return suite


if __name__ == "__main__":
    unittest.main(verbosity=2)


# End of file
