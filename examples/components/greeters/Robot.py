
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


class Robot(Greeter):

    model = pyre.inventory.str("model", default="X52")
    model.meta["tip"] = "Robot model name."

    def __init__(self):
        Greeter.__init__(self, name="robot")

    def _defaults(self):
        self.greeting = "Greetings human."

    def greet(self):
        print("{} I am a {} robot.".format(self.greeting, self.model))


def greeter():
    return Robot()


# End of file
