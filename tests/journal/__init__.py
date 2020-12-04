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

from . import test_facilities
from . import test_channels
from . import test_devices


def test_cases():
    tests = []
    for mod in [test_facilities, test_channels, test_devices]:
        tests += mod.test_classes()
    return tests


# End of file
