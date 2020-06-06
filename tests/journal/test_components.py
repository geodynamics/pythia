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

from journal.components.Journal import Journal


class TestJournal(unittest.TestCase):

    def test_firewall(self):
        from journal.diagnostics.Diagnostic import Diagnostic

        firewall = journal.firewall("test")
        with self.assertRaises(Diagnostic.Fatal):
            self._check_journal("firewall.log", "firewall", firewall)
        os.remove("firewall.log")

    def test_debug(self):
        debug = journal.debug("test")
        self._check_journal("debug.log", "debug", debug)

    def test_info(self):
        info = journal.info("test")
        self._check_journal("info.log", "info", info)

    def test_warning(self):
        warning = journal.warning("test")
        self._check_journal("warning.log", "warning", warning)

    def test_error(self):
        error = journal.error("test")
        self._check_journal("error.log", "error", error)


# End of file
