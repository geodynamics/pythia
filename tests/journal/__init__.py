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

import test_facilities
import test_channels
import test_devices


def test_cases():
    tests = [
        test_facilities.TestFacilities,
        test_channels.TestChannels,
        test_devices.TestDevices,
    ]
    return tests


# End of file
