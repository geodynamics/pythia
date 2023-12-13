#!/usr/bin/env python3
# ======================================================================
#
# Brad T. Aagaard, U.S. Geological Survey
# Charles A. Williams, GNS Science
# Matthew G. Knepley, University of Chicago
#
# This code was developed as part of the Computational Infrastructure
# for Geodynamics (http://geodynamics.org).
#
# Copyright (c) 2010-2017 University of California, Davis
#
# See COPYING for license information.
#
# ======================================================================

"""Script to run pythia (minus mpi) test suite.

Run `coverage report` to generate a report (included).
Run `coverage html -d DIR` to generate an HTML report in directory `DIR`.

Note: Pyre runs MPI in a subprocess which is not measured by coverage.
"""


import unittest
import sys


sys.path.append("./pyre")


def create_coverage():
    cov = None
    try:
        import coverage
        src_dirs = [
            "pythia.journal",
            "pythia.pyre.applications",
            "pythia.pyre.components",
            "pythia.pyre.filesystem",
            "pythia.pyre.inventory",
            "pythia.pyre.odb",
            "pythia.pyre.parsing",
            "pythia.pyre.schedulers",
            "pythia.pyre.units",
            "pythia.pyre.util",
            "pythia.pyre.xml",
        ]
        cov = coverage.Coverage(source=src_dirs)
        cov.start()
    except ImportError as ex:
        pass
    return cov

def close_coverage(cov):
    if cov:
        cov.stop()
        cov.save()
        cov.report()
        cov.xml_report(outfile="coverage.xml")


def load_tests(loader, tests, pattern):
    import pyre.test_units
    import pyre.test_inventory
    import pyre.test_schedulers
    import pyre.test_pyredoc
    import pyre.test_nemesis
    import journal.test_channels
    import journal.test_devices
    import journal.test_facilities
    
    suite = unittest.TestSuite()
    for mod in [
        pyre.test_units,
        pyre.test_inventory,
        pyre.test_schedulers,
        pyre.test_pyredoc,
        pyre.test_nemesis,
        journal.test_channels,
        journal.test_devices,
        journal.test_facilities,                
        ]:
        suite.addTests(loader.loadTestsFromModule(mod))
    return suite


def configureSubcomponents(facility):
    """Configure subcomponents."""
    for component in facility.components():
        configureSubcomponents(component)
        component._configure()
    return



# ----------------------------------------------------------------------
if __name__ == '__main__':
    cov = create_coverage()

    suite = load_tests(unittest.defaultTestLoader, tests=None, pattern=None)
    success = unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
    close_coverage(cov)
    if not success:
        sys.exit(1)


# End of file
