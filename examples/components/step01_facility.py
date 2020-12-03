#!/usr/bin/env python
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

import pyre.inventory
from pyre.applications.Script import Script


class GreeterApp(Script):
    """Greeter application with a single greeter."""

    from greeters.Greeter import Greeter
    greeter = pyre.inventory.facility("greeter", factory=Greeter)
    greeter.meta["tip"] = "Greeter for application."

    def __init__(self, name="greeterapp"):
        Script.__init__(self, name)

    def main(self, *args, **kwds):
        self.greeter.greet()


if __name__ == "__main__":
    GreeterApp().run()

# End of file
