
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

from .Greeter import Greeter
import pythia.pyre.inventory


class Human(Greeter):

    personName = pythia.pyre.inventory.str("name", default="John Doe")
    personName.meta["tip"] = "Name of person."

    def __init__(self):
        Greeter.__init__(self, name="human")

    def _defaults(self):
        self.greeting = "Hello."

    def greet(self):
        print("{} My name is {}.".format(self.greeting, self.personName))


def greeter():
    return Human()


# End of file
