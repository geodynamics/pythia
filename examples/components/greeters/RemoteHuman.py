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


class RemoteHuman(Component):

    greeting = pythia.pyre.inventory.str("greeting", default="Hello.")
    greeting.meta["tip"] = "Greeter message."

    personName = pythia.pyre.inventory.str("name", default="John Doe")
    personName.meta["tip"] = "Name of person."

    location = pythia.pyre.inventory.str("location", default="an island in the Pacific Ocean")
    location.meta["tip"] = "Location of person."

    technology = pythia.pyre.inventory.str("technology", default="satellite phone")
    technology.meta["tip"] = "Communication technology."

    def __init__(self):
        Component.__init__(self, name="remotehuman")

    def greet(self):
        print("{} This is {} coming to you from {} via {}.".format(
            self.greeting, self.personName, self.location, self.technology))


def greeter():
    return RemoteHuman()


# End of file
