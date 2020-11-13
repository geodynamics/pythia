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

import test_application
import test_communicator
import test_launcher


def test_cases():
    tests = [
        test_application.TestApplication,
        test_communicator.TestCommunicator,
        test_launcher.TestLauncher,
    ]
    return tests


# End of file
