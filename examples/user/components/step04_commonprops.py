#!/usr/bin/env python3
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

import sys

from pythia.pyre.applications.Script import Script
from pythia.pyre.components.Component import Component
import pythia.pyre.inventory

import greeters.Greeter

sys.path.append("./greeters")


def greeterFactory(name):
    return pythia.pyre.inventory.facility(name, family="greeter", vault=["greeters"], factory=greeters.Greeter.Greeter)


class TwoGreeters(Component):

    right = pythia.pyre.inventory.facility("right", family="greeter", vault=[
                                           "greeters"], factory=greeters.Greeter.Greeter)
    right.meta["tip"] = "Greeter 'right'."

    left = pythia.pyre.inventory.facility("left", family="greeter", vault=[
                                          "greeters"], factory=greeters.Greeter.Greeter)
    left.meta["tip"] = "Greeter 'left'."

    def __init__(self, name="twogreeters"):
        Component.__init__(self, name, facility="greeters")

    def components(self):
        return [self.left, self.right]


class GreeterApp(Script):
    """Greeter application with facility array."""

    greeters = pythia.pyre.inventory.facilityArray(
        "greeters", itemFactory=greeterFactory, factory=TwoGreeters)
    greeters.meta["tip"] = "Greeter for application."

    def __init__(self, name="greeterapp"):
        Script.__init__(self, name)

    def main(self, *args, **kwds):
        greeters = self.greeters.components()
        print("We have {:d} greetings for you:".format(len(greeters)))
        for greeter in greeters:
            greeter.greet()


if __name__ == "__main__":
    GreeterApp().run()

# End of file
