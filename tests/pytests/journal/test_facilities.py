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

from pythia.journal.diagnostics import (info, debug, warning, error, firewall)
from pythia.pyre.applications.Script import Script


class TestFacilities(unittest.TestCase):

    def test_console(self):
        app = JournalApp()
        args = [
            "--journal.debug.debug_on=1",
            "--journal.debug.debug_off=0",
        ]
        app.run(argv=["journalapp"] + args)

    def test_colorconsole(self):
        app = JournalApp()
        args = [
            "--journal.debug.debug_on=1",
            "--journal.debug.debug_off=0",
            "--journal.device=color-console",
        ]
        app.run(argv=["journalapp"] + args)

    def test_file(self):
        filename = "journalapp.log"

        app = JournalApp()
        args = [
            "--journal.debug.debug_on=1",
            "--journal.debug.debug_off=0",
            "--journal.device=file",
            "--journal.device.name={}".format(filename),
        ]
        app.run(argv=["journalapp"] + args)

        with open(filename, "r") as log:
            logLines = log.readlines()
            self.assertEqual(4, len(logLines))
            iLine = 2
            self.assertEqual("-- debug_on(debug)", logLines[iLine].strip())
            iLine += 1
            self.assertEqual("-- This journal should be on.", logLines[iLine].strip())
        os.remove(filename)


class JournalApp(Script):

    def __init__(self, name="journalapp"):
        Script.__init__(self, name)

    def main(self, *args, **kwds):
        debugOn = debug("debug_on")
        debugOn.activate()
        debugOn.log("This journal should be on.")
        debugOn.deactivate()
        debugOn.log("This journal should be off.")

        debugOff = debug("debug_off")
        debugOff.log("This journal should be off.")


def load_tests(loader, tests, pattern):
    TEST_CLASSES = [TestFacilities]

    suite = unittest.TestSuite()
    for cls in TEST_CLASSES:
        suite.addTests(loader.loadTestsFromTestCase(cls))
    return suite


if __name__ == "__main__":
    unittest.main(verbosity=2)


# End of file
