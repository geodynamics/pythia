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

import journal

class TestDevices(unittest.TestCase):

    def setUp(self):
        self.journal = journal.debug("test")
        self.journal.activate()
    
    def test_console(self):
        from journal.devices.Console import Console
        journal.journal().device = Console()
        self.journal.log("Hello")

    def test_colorconsole(self):
        from journal.devices.ANSIColorConsole import ANSIColorConsole
        journal.journal().device = ANSIColorConsole()
        self.journal.log("Hello")

    def test_textfile(self):
        from journal.devices.TextFile import TextFile

        filename = "debug.log"
        with open(filename, "w") as log:
            journal.journal().device = TextFile(log)
            self.journal.log("Hello")

        with open(filename, "r") as log:
            logLines = log.readlines()
            iLog = 1
            self.assertEqual(">> test(debug)", logLines[iLog].strip())
            iLog += 1
            self.assertEqual("-- Hello", logLines[iLog].strip())
            iLog += 1
        os.remove(filename)


# End of file
