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

import journal.diagnostics
from pyre.applications.Script import Script


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
        debugOn = journal.diagnostics.debug("debug_on")
        debugOn.activate()
        debugOn.log("This journal should be on.")
        debugOn.deactivate()
        debugOn.log("This journal should be off.")

        debugOff = journal.diagnostics.debug("debug_off")
        debugOff.log("This journal should be off.")


def test_classes():
    return [TestFacilities]


if __name__ == "__main__":
    suite = unittest.TestSuite()
    for cls in test_classes():
        suite.addTest(unittest.makeSuite(cls))
    unittest.TextTestRunner(verbosity=2).run(suite)


# End of file
