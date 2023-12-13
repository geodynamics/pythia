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
import subprocess

COLORCONSOLE_OUTPUT = \
"""No help available for module pythia.journal.components.ColorConsole.

No help available for class ColorConsole.
facilities of 'console':
    renderer=<component name>: the facility that controls how the messages are formatted
        current value: 'renderer', from {default}
        configurable as: renderer
properties of 'console':
    help=<bool>: prints a screen that describes my traits
        default value: False
        current value: False, from {default}
    help-components=<bool>: prints a screen that describes my subcomponents
        default value: False
        current value: False, from {default}
    help-persistence=<bool>: prints a screen that describes my persistent store
        default value: False
        current value: False, from {default}
    help-properties=<bool>: prints a screen that describes my properties
        default value: False
        current value: False, from {default}
"""

SCHEDULERLSF_OUTPUT = \
"""No help available for module pythia.pyre.schedulers.SchedulerLSF.

No help available for class SchedulerLSF.
facilities of 'lsf':
properties of 'lsf':
    bsub-options=<list>: (no documentation available)
        default value: []
        current value: [], from {default}
    command=<str>: (no documentation available)
        default value: 'bsub'
        current value: 'bsub', from {default}
    dry=<bool>: don't actually run the job; just print the batch script
        default value: False
        current value: False, from {default}
    help=<bool>: prints a screen that describes my traits
        default value: False
        current value: False, from {default}
    help-components=<bool>: prints a screen that describes my subcomponents
        default value: False
        current value: False, from {default}
    help-persistence=<bool>: prints a screen that describes my persistent store
        default value: False
        current value: False, from {default}
    help-properties=<bool>: prints a screen that describes my properties
        default value: False
        current value: False, from {default}
    shell=<str>: shell for #! line of batch scripts
        default value: '/bin/sh'
        current value: '/bin/sh', from {default}
    wait=<bool>: wait for the job to finish
        default value: False
        current value: False, from {default}
"""

class TestPyreDoc(unittest.TestCase):

    def test_colorconsole(self):
        process = subprocess.run(["pyre_doc.py", "pythia.journal.components.ColorConsole"], stdout=subprocess.PIPE)
        linesE = COLORCONSOLE_OUTPUT.split("\n")
        lines = process.stdout.decode("utf-8").split("\n")
        self.assertEqual(len(linesE), len(lines))
        for lineE, line in zip(linesE, lines):
            self.assertEqual(lineE, line)

    def test_schedulerlsf(self):
        process = subprocess.run(["pyre_doc.py", "pythia.pyre.schedulers.SchedulerLSF"], stdout=subprocess.PIPE)
        linesE = SCHEDULERLSF_OUTPUT.split("\n")
        lines = process.stdout.decode("utf-8").split("\n")
        self.assertEqual(len(linesE), len(lines))
        for lineE, line in zip(linesE, lines):
            self.assertEqual(lineE, line)


def load_tests(loader, tests, pattern):
    TEST_CLASSES = [TestPyreDoc]

    suite = unittest.TestSuite()
    for cls in TEST_CLASSES:
        suite.addTests(loader.loadTestsFromTestCase(cls))
    return suite


if __name__ == "__main__":
    unittest.main(verbosity=2)


# End of file
