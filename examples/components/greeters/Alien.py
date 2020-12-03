
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
import pyre.inventory


class Alien(Greeter):

    alienName = pyre.inventory.str("name", default="Zorg")
    alienName.meta["tip"] = "Name of alien."

    planet = pyre.inventory.str("planet", default="Zipium")
    planet.meta["tip"] = "Planet of origin."

    def __init__(self):
        Greeter.__init__(self, name="alien")

    def _defaults(self):
        self.greeting = "Greetings earthling."

    def greet(self):
        print("{} I am {} from the planet {}.".format(self.greeting, self.alienName, self.planet))


def greeter():
    return Alien()


# End of file
