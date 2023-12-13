#!/usr/bin/env nemesis
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

"""Script to run MPI test suite.

Code coverage is not reported because the code tested is actually
within the pyre.mpi module. Furthermore, Pyre runs MPI in a subprocess
which is not measured by coverage.
"""

import unittest


def configureSubcomponents(facility):
    """Configure subcomponents."""
    for component in facility.components():
        configureSubcomponents(component)
        component._configure()
    return

def load_tests(loader, tests, pattern):
    import mpi.test_application
    import mpi.test_communicator
    import mpi.test_launcher

    suite = unittest.TestSuite()
    for mod in [
        mpi.test_application,
        mpi.test_communicator,
        mpi.test_launcher,
        ]:
        suite.addTests(loader.loadTestsFromModule(mod))

    return suite



# ----------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main(verbosity=2)


# End of file
