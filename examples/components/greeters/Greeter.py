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

from pythia.pyre.components.Component import Component
import pythia.pyre.inventory


class Greeter(Component):

    greeting = pythia.pyre.inventory.str("greeting", default="Hello world!")
    greeting.meta["tip"] = "Greeter message."

    def __init__(self, name="greeter"):
        Component.__init__(self, name)

    def greet(self):
        print(self.greeting)


def greeter():
    return Greeter()


# End of file
