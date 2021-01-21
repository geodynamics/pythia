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

from pythia import journal
from pythia.journal import diagnostics
from pythia.journal import devices


class TestChannels(unittest.TestCase):

    def _check_journal(self, filename, name, diagnostic):
        lines = [
            "Line 0.",
            "Line 1.",
            "Line 2.",
        ]
        linesLog = [
            "Line 0.",
            "Line 2.",
        ]

        with open(filename, "w") as log:
            devices.logfile(log)
            i = 0
            diagnostic.activate()
            for line in lines:
                diagnostic.log(line)
                diagnostic.flip()

        with open(filename, "r") as log:
            logLines = log.readlines()
            iLog = 0
            for line in linesLog:
                iLog += 1
                self.assertEqual(">> test({name})".format(name=name), logLines[iLog].strip())
                iLog += 1
                self.assertEqual("-- {line}".format(line=line), logLines[iLog].strip())
                iLog += 1
        os.remove(filename)

    def test_firewall(self):
        from pythia.journal.diagnostics.Diagnostic import Diagnostic

        firewall = diagnostics.firewall("test")
        with self.assertRaises(Diagnostic.Fatal):
            self._check_journal("firewall.log", "firewall", firewall)
        os.remove("firewall.log")

    def test_debug(self):
        debug = diagnostics.debug("test")
        self._check_journal("debug.log", "debug", debug)

    def test_info(self):
        info = diagnostics.info("test")
        self._check_journal("info.log", "info", info)

    def test_warning(self):
        warning = diagnostics.warning("test")
        self._check_journal("warning.log", "warning", warning)

    def test_error(self):
        error = diagnostics.error("test")
        self._check_journal("error.log", "error", error)

    def test_channels(self):
        CHANNELS = ("firewall", "debug", "info", "warning", "error")
        j = journal.journal()
        channels = j.channels()
        self.assertEqual(len(CHANNELS), len(channels))
        for channel in channels:
            self.assertTrue(channel in CHANNELS)

    def test_entry(self):
        j = journal.journal()
        entry = j.entry()
        self.assertEqual({}, entry.meta)
        self.assertEqual([], entry.text)


def test_classes():
    return [TestChannels]


if __name__ == "__main__":
    suite = unittest.TestSuite()
    for cls in test_classes():
        suite.addTest(unittest.makeSuite(cls))
    unittest.TextTestRunner(verbosity=2).run(suite)


# End of file
