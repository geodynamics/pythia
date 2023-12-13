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
import subprocess




class TestNemesis(unittest.TestCase):

    def test_interpreter(self):
        greeting = "Hello world!"
        cmd = ["nemesis", "-c", "print('%s')" % greeting]
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(0, process.returncode)
        self.assertEqual(greeting.encode(encoding='UTF-8'), process.stdout.strip())


def load_tests(loader, tests, pattern):
    TEST_CLASSES = [TestNemesis]

    suite = unittest.TestSuite()
    for cls in TEST_CLASSES:
        suite.addTests(loader.loadTestsFromTestCase(cls))
    return suite


if __name__ == "__main__":
    unittest.main(verbosity=2)


# End of file
